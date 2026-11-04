"""
Validity-Aware Retriever for Hebbian Memory and Temporal Knowledge Base.
Integrates episodic retrieval with validity-aware semantic knowledge and explicit temporal grounding.

Reference:
- HeLa-Mem (ACL 2026): HebbianRetriever
- Formalized in relatorio_entrega1_enxuto_ieee.tex (Section I-B & I-C)
"""

import os
import sys
import numpy as np
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HELA_DIR = os.path.join(ROOT_DIR, "external", "HeLa-Mem")
if HELA_DIR not in sys.path:
    sys.path.insert(0, HELA_DIR)

from hela_mem.hebbian_memory import HebbianMemoryGraph
from hela_mem.utils import (
    gpt_generate_answer_with_rotation,
    compute_time_decay,
)
from hela_mem.eval_longmemeval import build_longmemeval_prompt as hela_original_prompt
from src.modeling.temporal_knowledge_memory import TemporalKnowledgeMemory, parse_date

ABLATIONS = ("none", "no_temporal")


class ValidityAwareRetriever:
    """
    Retriever that incorporates query timestamp t_query into both
    semantic fact pertinence and episodic temporal presentation.

    ablation="no_temporal" (B0): same facts and retrieval code, but the temporal
    mechanism is switched off in the knowledge memory and the prompt falls back to
    HeLa-Mem's original template (untagged "- fact" lines, original system prompt),
    i.e. exactly the Baseline A prompt fed with session-wise extracted facts.
    """

    def __init__(
        self,
        memory_graph: HebbianMemoryGraph,
        temporal_knowledge: Optional[TemporalKnowledgeMemory] = None,
        ablation: str = "none",
    ):
        if ablation not in ABLATIONS:
            raise ValueError(f"Unknown ablation '{ablation}'. Expected one of {ABLATIONS}.")
        self.graph = memory_graph
        self.temporal_kb = temporal_knowledge
        self.ablation = ablation
        if ablation == "no_temporal" and self.temporal_kb is not None:
            self.temporal_kb.disable_temporal_mechanism()

    def format_knowledge_base_text(
        self,
        kb_results: List[Dict[str, Any]],
        query_date_str: str = "",
    ) -> str:
        """
        Formats retrieved facts with explicit validity windows and status tags.
        Enables LLM to differentiate active facts from historical superseded facts.
        """
        if not kb_results:
            return ""

        if self.ablation == "no_temporal":
            # HeLa-Mem original format (eval_longmemeval.answer_question)
            return "\n".join(f"- {kn.get('knowledge', '')}" for kn in kb_results)

        lines = []
        for kn in kb_results:
            status = kn.get("status", "active")
            v_from = kn.get("valid_from", "unknown")
            v_to = kn.get("valid_to")
            content = kn.get("knowledge", "")

            if status == "active" or v_to is None:
                tag = f"[CURRENT / ACTIVE (Valid since: {v_from})]"
            else:
                tag = f"[HISTORICAL / SUPERSEDED (Valid: {v_from} to {v_to})]"

            lines.append(f"- {tag} {content}")

        return "\n".join(lines)

    def retrieve_episodic(
        self,
        query: str,
        query_date: Optional[str] = None,
        top_k: int = 15,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves episodic nodes using HeLa-Mem's original dual-pathway retrieval
        (vector similarity + spreading activation) untouched.
        """
        return self.graph.retrieve(query, top_k=top_k)

    def build_longmemeval_prompt(
        self,
        context_text: str,
        knowledge_text: str,
        profile_text: str,
        assistant_knowledge_text: str,
        question: str,
        question_date: str,
    ) -> Tuple[str, str]:
        """
        Builds the prompt pair (system_prompt, user_prompt) following
        the exact template of HeLa-Mem, with enhanced knowledge base grounding.
        """
        if self.ablation == "no_temporal":
            return hela_original_prompt(
                context_text, knowledge_text, profile_text,
                assistant_knowledge_text, question, question_date,
            )

        system_prompt = (
            "You are a helpful assistant with access to the user's conversation history and structured knowledge base.\n"
            "Your task is to answer questions about the user or past conversations in an extremely concise manner.\n"
            "When memories or facts conflict over time, use the KNOWLEDGE BASE status tags: prioritize the CURRENT / ACTIVE state for current questions, and refer to HISTORICAL / SUPERSEDED facts when asked about earlier, initial, or past states.\n"
            "When the question is: \"What did the charity race raise awareness for?\", "
            "you should not answer in the form of: \"The charity race raised awareness "
            "for mental health.\" Instead, it should be: \"mental health\", as this is "
            "more concise."
        )
        if assistant_knowledge_text:
            system_prompt += f"\n{assistant_knowledge_text}"

        user_prompt = (
            f"<CONTEXT>\n"
            f"Current date: {question_date}\n\n"
            f"Relevant memories from conversation history:\n"
            f"{context_text}\n\n"
        )

        if knowledge_text:
            user_prompt += f"<KNOWLEDGE BASE>\n{knowledge_text}\n\n"

        if profile_text and profile_text != "None":
            user_prompt += f"<CHARACTER TRAITS>\nCharacteristics of the user:\n{profile_text}\n\n"

        user_prompt += (
            f"Question: {question}\n"
            f"Please only provide the content of the answer, without including 'answer:'\n"
            f"For questions that require answering a date or time, strictly follow the "
            f"format \"15 July 2023\" and provide a specific date whenever possible. "
            f"For example, if you need to answer \"last year,\" give the specific year "
            f"rather than just saying \"last year.\" Only provide one year, date, or time, "
            f"without any extra responses.\n"
            f"If the question is about the duration, answer in the form of several years, "
            f"months, or days.\n"
            f"Generate answers primarily composed of concrete entities."
        )

        return system_prompt, user_prompt

    def answer_question(
        self,
        question: str,
        question_date: str,
        top_k: int = 15,
        semantic_top_k: int = 5,
        item_id: str = "",
    ) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        End-to-end question answering pipeline:
        1. Episodic retrieval with query-date anchoring
        2. Semantic retrieval from TemporalKnowledgeMemory with validity scoring
        3. Explicit prompt synthesis and generation via LLM
        """
        # 1. Episodic retrieval
        episodic_results = self.retrieve_episodic(question, query_date=question_date, top_k=top_k)

        context_blocks = []
        for res in episodic_results[:top_k]:
            node = res["node"]
            score = res.get("score", 0.0)
            source_label = "Direct Match" if res.get("base_score", 0) > 0.6 else "Associative Memory"
            block = (
                f"[{source_label} | Relevancy: {score:.2f}]\n"
                f"Time: {node.get('timestamp', 'unknown')}\n"
                f"Content: {node.get('content', '')}"
            )
            context_blocks.append(block)

        context_text = "\n\n".join(context_blocks)

        # 2. Semantic retrieval from Temporal Knowledge Memory
        semantic_results = []
        knowledge_text = ""
        if self.temporal_kb:
            try:
                semantic_results = self.temporal_kb.search_knowledge(
                    question, query_date=question_date, top_k=semantic_top_k
                )
                knowledge_text = self.format_knowledge_base_text(
                    semantic_results, query_date_str=question_date
                )
            except Exception as e:
                print(f"    [{item_id}] Semantic retrieval error: {e}")

        # 3. User profile and assistant knowledge
        profile_text = "None"
        assistant_knowledge_text = ""
        if self.temporal_kb:
            profile_text = self.temporal_kb.get_raw_user_profile(item_id) or "None"
            try:
                ak_list = self.temporal_kb.get_assistant_knowledge()
                if ak_list:
                    assistant_knowledge_text = "Here are some of your character traits and knowledge:\n"
                    for ak_item in ak_list:
                        k_text = ak_item.get("knowledge", "").strip()
                        if k_text:
                            assistant_knowledge_text += f"- {k_text}\n"
            except Exception as e:
                print(f"    [{item_id}] Assistant knowledge error: {e}")

        # 4. Generate answer
        system_prompt, user_prompt = self.build_longmemeval_prompt(
            context_text,
            knowledge_text,
            profile_text,
            assistant_knowledge_text,
            question,
            question_date,
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = gpt_generate_answer_with_rotation(user_prompt, messages)
        return response, episodic_results, semantic_results
