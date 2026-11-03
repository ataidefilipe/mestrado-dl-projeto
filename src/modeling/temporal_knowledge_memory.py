"""
Temporal Knowledge Memory with Validity Windows and Fact Supersession.
Extends HeLa-Mem's semantic memory architecture (HebbianKnowledgeMemory)
by incorporating explicit validity intervals [valid_from, valid_to] and supersession links.

Reference:
- Chauhan et al. (2025): Zep / Graphiti Temporal Knowledge Graphs
- Bro et al. (2026): HeLa-Mem Semantic Memory Store
"""

import os
import sys
import json
import re
import numpy as np
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# Ensure HeLa-Mem can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HELA_DIR = os.path.join(ROOT_DIR, "external", "HeLa-Mem")
if HELA_DIR not in sys.path:
    sys.path.insert(0, HELA_DIR)

from hela_mem.hebbian_memory import HebbianMemoryGraph
from hela_mem.utils import (
    get_timestamp,
    get_embedding,
    normalize_vector,
    _create_client,
    gpt_generate_answer,
)


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    Robust datetime parser supporting LongMemEval formats:
    - '2023/05/20 (Sat) 12:36'
    - '2023-05-20 12:36:00'
    - '2023/05/20'
    - '2023-05-20'
    """
    if not date_str or not isinstance(date_str, str):
        return None
    # Strip day of week in parentheses like '(Sat)'
    clean = re.sub(r"\s*\([A-Za-z]+\)\s*", " ", date_str).strip()
    formats = (
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d",
        "%Y-%m-%d",
    )
    for fmt in formats:
        try:
            return datetime.strptime(clean, fmt)
        except ValueError:
            pass
    return None


class TemporalKnowledgeMemory:
    """
    Semantic Memory with Temporal Validity Windows and Supersession.
    Maintains a dynamic graph of knowledge nodes with:
    - valid_from (t_start): session timestamp when fact was observed
    - valid_to (t_end): timestamp when fact was superseded (None if active)
    - status: 'active' or 'superseded'
    - superseded_by: node_id of newer replacement fact
    - supersedes: list of node_ids replaced by this fact
    """

    def __init__(
        self,
        file_path: str = "temporal_long_term.json",
        max_capacity: int = 100,
        tau_decay_seconds: float = 60 * 86400,  # 60 days default (from HeLa-Mem paper)
        lambda_sim: float = 0.6,                # Balance vector sim vs temporal validity
        supersede_sim_threshold: float = 0.35,  # Candidate threshold for supersession check
    ):
        self.file_path = file_path
        self.max_capacity = max_capacity
        self.tau_decay = float(os.environ.get("TEMPORAL_TAU_DECAY", tau_decay_seconds))
        self.lambda_sim = float(os.environ.get("TEMPORAL_LAMBDA", lambda_sim))
        self.supersede_sim_threshold = float(
            os.environ.get("TEMPORAL_SUPERSEDE_SIM_THRESHOLD", supersede_sim_threshold)
        )

        self.user_profiles: Dict[str, Any] = {}
        self.assistant_knowledge: List[Dict[str, Any]] = []
        self.fallback_kb: List[Dict[str, Any]] = []

        # Hebbian Graph for Semantic Knowledge Base
        self.hebbian_kb_path = file_path.replace(".json", "_kb_graph.json")
        self.knowledge_graph = HebbianMemoryGraph(self.hebbian_kb_path)

        self.load()

    def update_user_profile(self, user_id: str, new_data: Any, merge: bool = False) -> None:
        """Update user profile compatible with HeLa-Mem interface."""
        if merge and user_id in self.user_profiles:
            current_data = self.user_profiles[user_id]["data"]
            if isinstance(current_data, str) and isinstance(new_data, str):
                updated_data = f"{current_data}\n\n--- Updated ---\n{new_data}"
            else:
                updated_data = new_data
        else:
            updated_data = new_data

        self.user_profiles[user_id] = {
            "data": updated_data,
            "last_updated": get_timestamp(),
        }
        self.save()

    def get_raw_user_profile(self, user_id: str) -> str:
        return self.user_profiles.get(user_id, {}).get("data", "")

    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        return self.user_profiles.get(user_id, {})

    def add_assistant_knowledge(self, knowledge_text: str) -> None:
        if not knowledge_text or knowledge_text.strip() in ("", "- None", "- None."):
            return
        vec = get_embedding(knowledge_text)
        vec = normalize_vector(vec).tolist()
        entry = {
            "knowledge": knowledge_text,
            "timestamp": get_timestamp(),
            "knowledge_embedding": vec,
        }
        self.assistant_knowledge.append(entry)
        if len(self.assistant_knowledge) > self.max_capacity:
            self.assistant_knowledge = self.assistant_knowledge[-self.max_capacity:]
        self.save()

    def get_assistant_knowledge(self) -> List[Dict[str, Any]]:
        return self.assistant_knowledge

    def classify_relation(
        self,
        earlier_fact: str,
        earlier_time: str,
        new_fact: str,
        new_time: str,
        client: Any = None,
    ) -> str:
        """
        Classifies relationship between an earlier fact and a new fact:
        Returns: 'SUPERSEDES', 'EXTENDS', or 'UNRELATED'
        """
        prompt = (
            "You are a factual consistency and temporal update classifier.\n"
            "Analyze whether a newly observed fact updates, replaces, or alters an earlier recorded fact "
            "about a user's belongings, habits, plans, status, or preferences.\n\n"
            f"EARLIER FACT (Recorded on {earlier_time}):\n\"{earlier_fact}\"\n\n"
            f"NEW FACT (Recorded on {new_time}):\n\"{new_fact}\"\n\n"
            "GUIDELINES:\n"
            "- SUPERSEDES: The new fact updates, replaces, or changes the state, location, plan, preference, "
            "or condition regarding an entity, item, or topic from the earlier fact (e.g., moving an item to a new storage "
            "location, changing a job, altering a plan, adopting a new preference). Even if phrased as a plan, "
            "if it establishes a new state for that item or topic, it supersedes the earlier state.\n"
            "- EXTENDS: Both facts are simultaneously true, compatible, and describe different non-conflicting aspects.\n"
            "- UNRELATED: The facts refer to completely different entities or unrelated topics.\n\n"
            "Output format:\n"
            "Reasoning: <1 sentence explanation>\n"
            "Classification: <SUPERSEDES, EXTENDS, or UNRELATED>"
        )
        messages = [
            {"role": "system", "content": "You are a precise factual update classifier."},
            {"role": "user", "content": prompt},
        ]
        actual_client = getattr(client, "client", client)
        try:
            resp = gpt_generate_answer(prompt, messages, client=actual_client, model=os.environ.get("HEBBIAN_MODEL", "gpt-4o-mini"))
            resp_upper = resp.upper()
            if "SUPER" in resp_upper:
                return "SUPERSEDES"
            if "EXTEND" in resp_upper:
                return "EXTENDS"
            return "UNRELATED"
        except Exception as e:
            print(f"    [RelationClassifier Error] {e}")
            return "UNRELATED"

    def add_knowledge(
        self,
        knowledge_text: str,
        event_timestamp: Optional[str] = None,
        client: Any = None,
    ) -> str:
        """
        Adds a knowledge fact with temporal validity and supersession checking.
        """
        if not knowledge_text or knowledge_text.strip() in ("", "- None", "- None."):
            return ""

        ts = event_timestamp or get_timestamp()
        norm_emb = normalize_vector(get_embedding(knowledge_text))

        # Check existing active facts for candidates
        nodes = self.knowledge_graph.nodes
        active_candidates = []

        for nid, node in nodes.items():
            meta = node.get("metadata", {})
            cand_time = node.get("timestamp")

            # Facts from the same session dialogue do not supersede each other
            if cand_time and ts and cand_time == ts:
                continue

            if meta.get("status", "active") == "active" and meta.get("valid_to") is None:
                emb = np.array(node["embedding"], dtype=np.float32)
                sim = float(norm_emb @ emb)
                if sim >= self.supersede_sim_threshold:
                    active_candidates.append((nid, node, sim))

        active_candidates.sort(key=lambda x: x[2], reverse=True)

        new_node_id = str(len(nodes))
        superseded_ids = []

        # Check relationship against top candidates
        for cand_id, cand_node, sim in active_candidates[:4]:
            cand_time = cand_node.get("timestamp", "earlier")
            cand_text = cand_node["content"]

            relation = self.classify_relation(
                earlier_fact=cand_text,
                earlier_time=cand_time,
                new_fact=knowledge_text,
                new_time=ts,
                client=client,
            )

            if relation == "SUPERSEDES":
                # Close earlier fact validity
                cand_node["metadata"]["valid_to"] = ts
                cand_node["metadata"]["status"] = "superseded"
                cand_node["metadata"]["superseded_by"] = new_node_id
                superseded_ids.append(cand_id)

                # Connect in knowledge graph
                self.knowledge_graph.add_edge(cand_id, new_node_id, weight=0.8, bidirectional=True)
                print(f"    [TemporalKB] Fact {new_node_id} SUPERSEDES {cand_id}: '{cand_text[:40]}...' -> '{knowledge_text[:40]}...'")

            elif relation == "EXTENDS":
                # Reinforce association
                self.knowledge_graph.add_edge(cand_id, new_node_id, weight=self.knowledge_graph.learning_rate, bidirectional=True)

        # Create new node
        new_node = {
            "id": new_node_id,
            "content": knowledge_text,
            "role": "system",
            "embedding": norm_emb.tolist(),
            "timestamp": ts,
            "metadata": {
                "type": "fact",
                "valid_from": ts,
                "valid_to": None,
                "status": "active",
                "superseded_by": None,
                "supersedes": superseded_ids,
            },
        }
        self.knowledge_graph.nodes[new_node_id] = new_node

        # Temporal chain to previous node (HeLa-Mem standard)
        if len(self.knowledge_graph.nodes) > 1:
            prev_id = str(len(self.knowledge_graph.nodes) - 2)
            self.knowledge_graph.add_edge(prev_id, new_node_id, weight=0.5, bidirectional=True)

        self.knowledge_graph.save()
        self.save()
        return new_node_id

    def compute_temporal_pertinence(
        self,
        node_metadata: Dict[str, Any],
        query_date_str: Optional[str],
    ) -> float:
        """
        Calculates temporal pertinence V(f_i, t_query):
        1.0: if valid_from <= t_query <= valid_to (or valid_to is None)
        exp(-|t_query - valid_to| / tau): if t_query > valid_to (superseded/expired)
        0.0: if t_query < valid_from (future)
        """
        if not query_date_str:
            return 1.0

        t_q = parse_date(query_date_str)
        if t_q is None:
            return 1.0

        v_from = parse_date(node_metadata.get("valid_from"))
        v_to = parse_date(node_metadata.get("valid_to"))

        if v_from and t_q < v_from:
            return 0.0  # Future fact

        if v_to is not None and t_q > v_to:
            delta_seconds = (t_q - v_to).total_seconds()
            if delta_seconds > 0:
                return float(np.exp(-delta_seconds / self.tau_decay))

        return 1.0  # Active during query date

    def search_knowledge(
        self,
        query: str,
        query_date: Optional[str] = None,
        top_k: int = 5,
        threshold: float = 0.1,
    ) -> List[Dict[str, Any]]:
        """
        Validity-Aware Semantic Retrieval.
        Combines Semantic Similarity, Temporal Pertinence V(f_i, t_query), and Spreading Activation.
        """
        nodes = self.knowledge_graph.nodes
        if not nodes:
            return []

        query_vec = normalize_vector(get_embedding(query))
        node_ids = list(nodes.keys())
        node_matrix = np.array([nodes[nid]["embedding"] for nid in node_ids], dtype=np.float32)

        # 1. Cosine similarity
        cos_sims = np.dot(node_matrix, query_vec)
        norm_sims = (cos_sims + 1.0) / 2.0  # scale [-1, 1] -> [0, 1]

        # 2. Temporal pertinence
        v_scores = np.zeros(len(node_ids), dtype=np.float32)
        for i, nid in enumerate(node_ids):
            v_scores[i] = self.compute_temporal_pertinence(
                nodes[nid].get("metadata", {}), query_date
            )

        # 3. Base combined score: lambda * Sim + (1 - lambda) * V
        base_scores = (self.lambda_sim * norm_sims) + ((1.0 - self.lambda_sim) * v_scores)

        # 4. Spreading Activation along Hebbian edges
        final_scores = base_scores.copy()
        id_to_idx = {nid: i for i, nid in enumerate(node_ids)}
        edges = self.knowledge_graph.edges
        alpha = self.knowledge_graph.activation_alpha
        spread_thresh = self.knowledge_graph.spreading_threshold

        for i, b_score in enumerate(base_scores):
            if b_score > spread_thresh:
                src_id = node_ids[i]
                for tgt_id, weight in edges.get(src_id, {}).items():
                    if tgt_id in id_to_idx:
                        tgt_idx = id_to_idx[tgt_id]
                        final_scores[tgt_idx] += b_score * weight * alpha

        # 5. Top-K ranking
        top_indices = np.argsort(final_scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            nid = node_ids[idx]
            node = nodes[nid]
            meta = node.get("metadata", {})
            results.append({
                "id": nid,
                "knowledge": node["content"],
                "timestamp": node.get("timestamp", ""),
                "score": float(final_scores[idx]),
                "base_score": float(base_scores[idx]),
                "sim": float(norm_sims[idx]),
                "temporal_pertinence": float(v_scores[idx]),
                "status": meta.get("status", "active"),
                "valid_from": meta.get("valid_from"),
                "valid_to": meta.get("valid_to"),
                "superseded_by": meta.get("superseded_by"),
                "supersedes": meta.get("supersedes", []),
            })

        return results

    def save(self) -> None:
        data = {
            "user_profiles": self.user_profiles,
            "assistant_knowledge": self.assistant_knowledge,
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.knowledge_graph.save()

    def load(self) -> None:
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.user_profiles = data.get("user_profiles", {})
                    self.assistant_knowledge = data.get("assistant_knowledge", [])
        except Exception as e:
            print(f"TemporalKB: Error loading data: {e}")
            self.user_profiles = {}
            self.assistant_knowledge = []
