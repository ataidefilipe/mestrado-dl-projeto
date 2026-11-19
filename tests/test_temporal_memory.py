"""
Unit tests for TemporalKnowledgeMemory, ValidityAwareRetriever ablations,
and paired statistical helpers (zero API calls, zero embedding downloads).

Run with:
    python -m unittest discover -s tests -v
"""

import math
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "external" / "HeLa-Mem"))

from hela_mem.hebbian_memory import HebbianMemoryGraph
from src.analysis.compare_ablation import mcnemar_exact
from src.modeling.temporal_knowledge_memory import TemporalKnowledgeMemory, parse_date
from src.modeling.validity_aware_retriever import ABLATIONS, ValidityAwareRetriever


class TestDateParsing(unittest.TestCase):
    def test_longmemeval_formats(self):
        dt = parse_date("2023/05/20 (Sat) 12:36")
        self.assertIsNotNone(dt)
        self.assertEqual((dt.year, dt.month, dt.day, dt.hour, dt.minute), (2023, 5, 20, 12, 36))

        dt2 = parse_date("2023-05-20 12:36:00")
        self.assertEqual((dt2.year, dt2.month, dt2.day), (2023, 5, 20))

        dt3 = parse_date("2023/05/20")
        self.assertEqual((dt3.year, dt3.month, dt3.day), (2023, 5, 20))

        self.assertIsNone(parse_date(None))
        self.assertIsNone(parse_date(""))
        self.assertIsNone(parse_date("not-a-date"))


class TestTemporalPertinenceAndAblations(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kb_path = os.path.join(self.tmp.name, "kb.json")
        self.mem_path = os.path.join(self.tmp.name, "mem.json")
        self.kb = TemporalKnowledgeMemory(
            file_path=self.kb_path,
            tau_decay_seconds=60 * 86400,
            lambda_sim=0.6,
        )
        self.graph = HebbianMemoryGraph(file_path=self.mem_path)

        # Populate two synthetic nodes directly in memory (no embedding/API call)
        self.kb.knowledge_graph.nodes["0"] = {
            "id": "0",
            "content": "User has 1250 followers on Instagram.",
            "role": "system",
            "embedding": [1.0, 0.0, 0.0],
            "timestamp": "2023/05/01 (Mon) 08:00",
            "metadata": {
                "type": "fact",
                "valid_from": "2023/05/01 (Mon) 08:00",
                "valid_to": "2023/05/10 (Wed) 08:00",
                "status": "superseded",
                "superseded_by": "1",
                "supersedes": [],
            },
        }
        self.kb.knowledge_graph.nodes["1"] = {
            "id": "1",
            "content": "User has 1300 followers on Instagram.",
            "role": "system",
            "embedding": [0.9, 0.43589, 0.0],
            "timestamp": "2023/05/10 (Wed) 08:00",
            "metadata": {
                "type": "fact",
                "valid_from": "2023/05/10 (Wed) 08:00",
                "valid_to": None,
                "status": "active",
                "superseded_by": None,
                "supersedes": ["0"],
            },
        }
        self.kb.knowledge_graph.add_edge("0", "1", weight=0.8, bidirectional=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_compute_temporal_pertinence_regimes(self):
        sup_meta = self.kb.knowledge_graph.nodes["0"]["metadata"]
        act_meta = self.kb.knowledge_graph.nodes["1"]["metadata"]

        # Active fact during query
        self.assertAlmostEqual(
            self.kb.compute_temporal_pertinence(act_meta, "2023/06/09 (Fri) 08:00"),
            1.0,
            places=6,
        )
        # Superseded fact 30 days after valid_to (tau = 60d -> exp(-0.5))
        v_30d = self.kb.compute_temporal_pertinence(sup_meta, "2023/06/09 (Fri) 08:00")
        self.assertAlmostEqual(v_30d, math.exp(-0.5), places=5)

        # Historical query inside [valid_from, valid_to] -> 1.0
        self.assertAlmostEqual(
            self.kb.compute_temporal_pertinence(sup_meta, "2023/05/05 (Fri) 08:00"),
            1.0,
            places=6,
        )
        # Future fact relative to query -> 0.0
        self.assertAlmostEqual(
            self.kb.compute_temporal_pertinence(act_meta, "2023/05/05 (Fri) 08:00"),
            0.0,
            places=6,
        )

    def test_ablation_no_temporal_b0(self):
        ret = ValidityAwareRetriever(self.graph, self.kb, ablation="no_temporal")
        # Metadata reset to active and V fixed at 1.0
        sup_meta = self.kb.knowledge_graph.nodes["0"]["metadata"]
        self.assertEqual(sup_meta["status"], "active")
        self.assertIsNone(sup_meta["valid_to"])
        self.assertAlmostEqual(
            self.kb.compute_temporal_pertinence(sup_meta, "2023/07/10 (Mon) 08:00"),
            1.0,
        )
        # Edges reset to standard 0.5 chain
        self.assertAlmostEqual(self.kb.knowledge_graph.edges["0"]["1"], 0.5)
        # Save guard prevents overwriting encoded Proposal B files
        with self.assertRaises(RuntimeError):
            self.kb.save()
        # Prompt formatting uses original untagged format
        formatted = ret.format_knowledge_base_text([{"knowledge": "Fact A", "status": "superseded", "valid_to": "2023/05/10"}])
        self.assertEqual(formatted, "- Fact A")

    def test_ablation_score_only(self):
        ret = ValidityAwareRetriever(self.graph, self.kb, ablation="score_only")
        sup_meta = self.kb.knowledge_graph.nodes["0"]["metadata"]
        # Pertinence remains active (< 1.0 after valid_to)
        self.assertLess(
            self.kb.compute_temporal_pertinence(sup_meta, "2023/07/10 (Mon) 08:00"),
            1.0,
        )
        # Prompt formatting strips tags
        formatted = ret.format_knowledge_base_text([{"knowledge": "Fact A", "status": "superseded", "valid_to": "2023/05/10"}])
        self.assertEqual(formatted, "- Fact A")
        sys_p, _ = ret.build_longmemeval_prompt("ctx", formatted, "None", "", "Q?", "2023/07/10")
        self.assertNotIn("status tags", sys_p)

    def test_ablation_tags_only(self):
        ret = ValidityAwareRetriever(self.graph, self.kb, ablation="tags_only")
        sup_meta = self.kb.knowledge_graph.nodes["0"]["metadata"]
        # Pertinence fixed at 1.0, but metadata status remains 'superseded'
        self.assertEqual(sup_meta["status"], "superseded")
        self.assertAlmostEqual(
            self.kb.compute_temporal_pertinence(sup_meta, "2023/07/10 (Mon) 08:00"),
            1.0,
        )
        # Save guard active
        with self.assertRaises(RuntimeError):
            self.kb.save()
        # Prompt formatting preserves tags and temporal system instruction
        formatted = ret.format_knowledge_base_text([
            {"knowledge": "Fact A", "status": "superseded", "valid_from": "2023/05/01", "valid_to": "2023/05/10"},
            {"knowledge": "Fact B", "status": "active", "valid_from": "2023/05/10", "valid_to": None},
        ])
        self.assertIn("[HISTORICAL / SUPERSEDED", formatted)
        self.assertIn("[CURRENT / ACTIVE", formatted)
        sys_p, _ = ret.build_longmemeval_prompt("ctx", formatted, "None", "", "Q?", "2023/07/10")
        self.assertIn("status tags", sys_p)

    def test_invalid_ablation_raises(self):
        self.assertEqual(set(ABLATIONS), {"none", "no_temporal", "score_only", "tags_only"})
        with self.assertRaises(ValueError):
            ValidityAwareRetriever(self.graph, self.kb, ablation="invalid_mode")


class TestStatistics(unittest.TestCase):
    def test_mcnemar_exact(self):
        # 14 gains, 0 regressions -> two-sided p = 2 * (0.5 ** 14) = 0.0001220703125
        p1, p2 = mcnemar_exact(14, 0)
        self.assertAlmostEqual(p1, 0.5 ** 14, places=10)
        self.assertAlmostEqual(p2, 2 * (0.5 ** 14), places=10)

        # Equal gains and regressions -> p = 1.0
        p1_eq, p2_eq = mcnemar_exact(10, 10)
        self.assertAlmostEqual(p2_eq, 1.0, places=10)

        # Zero discordant pairs -> p = 1.0
        self.assertEqual(mcnemar_exact(0, 0), (1.0, 1.0))


if __name__ == "__main__":
    unittest.main()
