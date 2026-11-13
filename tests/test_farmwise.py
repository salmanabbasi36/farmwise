"""Run from the project root:  python -m unittest discover -s tests -v"""
import json
import sys
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from farmwise import guardrails, weather  # noqa: E402
from farmwise.advisor import Advisor  # noqa: E402
from farmwise.retriever import BM25, stem, tokenize  # noqa: E402
from farmwise.web import make_handler  # noqa: E402


class RetrieverTests(unittest.TestCase):
    def test_stem_and_stopwords(self):
        self.assertEqual(stem("worms"), "worm")
        self.assertEqual(stem("yellowing"), "yellow")
        self.assertEqual(tokenize("How do I store the maize?"), ["store", "maize"])

    def test_bm25_ranks_relevant_doc_first(self):
        idx = BM25(["armyworm eats maize leaves", "store dry grain in bags", "plant when rains start"])
        self.assertEqual(idx.search("how to store grain")[0].index, 1)

    def test_no_match_returns_empty(self):
        self.assertEqual(BM25(["maize"]).search("football"), [])


class GuardrailTests(unittest.TestCase):
    def test_pesticide_dose_refused(self):
        self.assertEqual(guardrails.check("how many ml of insecticide per litre").action, "refuse")

    def test_fertilizer_rate_not_blocked(self):
        self.assertEqual(guardrails.check("how much DAP fertilizer at planting").action, "pass")

    def test_poisoning_is_emergency(self):
        self.assertEqual(guardrails.check("my brother swallowed pesticide").action, "emergency")

    def test_out_of_scope_topics(self):
        for q in ("my goats are sick", "I need a loan", "what is the market price of maize"):
            self.assertEqual(guardrails.check(q).action, "out_of_scope", q)

    def test_empty(self):
        self.assertEqual(guardrails.check("  ").action, "empty")

    def test_word_boundaries(self):
        # 'program' contains 'gram' and must not trigger the dose rule
        self.assertEqual(guardrails.check("is there a spray program for maize").action, "pass")


class AdvisorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adv = Advisor()

    def test_kb_integrity(self):
        ids = [e["id"] for e in self.adv.entries]
        self.assertEqual(len(ids), len(set(ids)))
        for e in self.adv.entries:
            for key in ("id", "title", "keywords", "steps", "caution", "source", "validated"):
                self.assertIn(key, e)
            self.assertTrue(e["steps"])

    def test_armyworm_question(self):
        ans = self.adv.ask("worms are eating my maize leaves")
        self.assertEqual(ans.status, "answer")
        self.assertEqual(ans.doc_ids[0], "fall_armyworm")
        self.assertIn("not yet validated", ans.text)
        self.assertIn("extension officer", ans.text)

    def test_unrelated_question_abstains(self):
        ans = self.adv.ask("who won the football match")
        self.assertEqual(ans.status, "abstain")
        self.assertEqual(ans.doc_ids, [])

    def test_dose_question_never_reaches_kb(self):
        ans = self.adv.ask("how much insecticide do I mix for armyworm")
        self.assertEqual(ans.status, "refuse")
        self.assertEqual(ans.doc_ids, [])

    def test_sms_format_is_short(self):
        ans = self.adv.ask("how do I store maize to stop weevils")
        sms = Advisor.format_sms(ans)
        self.assertLessEqual(len(sms), 320)
        self.assertIn("extension", sms.lower() + " extension" if sms.endswith("...") else sms.lower())


class WeatherTests(unittest.TestCase):
    def test_planting_signal_levels(self):
        self.assertEqual(weather.planting_signal([0, 0, 1, 0, 0, 2, 0])["level"], "wait")
        self.assertEqual(weather.planting_signal([10, 8, 0, 6, 5, 0, 0])["level"], "go")
        self.assertEqual(weather.planting_signal([15, 0, 0, 0, 0, 0, 0])["level"], "watch")

    def test_signal_reports_totals(self):
        s = weather.planting_signal([5, 5, 0.5])
        self.assertEqual(s["total_mm"], 10.5)
        self.assertEqual(s["wet_days"], 2)


class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(Advisor(), None))
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _post(self, path, payload):
        req = urllib.request.Request(self.base + path, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.load(r)

    def test_index_and_health(self):
        with urllib.request.urlopen(self.base + "/", timeout=5) as r:
            self.assertIn(b"FarmWise", r.read())
        with urllib.request.urlopen(self.base + "/api/health", timeout=5) as r:
            self.assertTrue(json.load(r)["ok"])

    def test_ask_endpoint(self):
        j = self._post("/api/ask", {"question": "when should I harvest my maize"})
        self.assertEqual(j["status"], "answer")
        self.assertEqual(j["doc_ids"][0], "harvest_timing")

    def test_ask_sms_channel(self):
        j = self._post("/api/ask", {"question": "when should I harvest my maize", "channel": "sms"})
        self.assertLessEqual(len(j["text"]), 320)


if __name__ == "__main__":
    unittest.main()
