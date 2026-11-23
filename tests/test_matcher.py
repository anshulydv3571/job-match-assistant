import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from matcher import clean_text, missing_keywords, rank_jobs

RESUME = "Python developer with pandas, SQL and MySQL. Built dashboards using Streamlit."


class TestMatcher(unittest.TestCase):
    def test_clean_text_keeps_tech_symbols(self):
        self.assertEqual(clean_text("Node.js, C++ & SQL!"), "node.js c++ sql")

    def test_full_stop_does_not_break_matching(self):
        missing = missing_keywords("I know MySQL.", "Needs mysql and tableau skills")
        self.assertNotIn("mysql", missing)
        self.assertIn("tableau", missing)

    def test_relevant_job_ranks_first(self):
        jobs = {
            "data.txt": "Looking for a Python and SQL developer to build pandas dashboards.",
            "chef.txt": "Hiring a head chef to run a busy restaurant kitchen and plan menus.",
        }
        ranked = rank_jobs(RESUME, jobs)
        self.assertEqual(ranked[0][0], "data.txt")
        self.assertGreater(ranked[0][1], ranked[1][1])

    def test_empty_jobs(self):
        self.assertEqual(rank_jobs(RESUME, {}), [])

    def test_missing_keywords_finds_gaps(self):
        job = "We need Python, Docker and Kubernetes experience for deployment work."
        missing = missing_keywords(RESUME, job)
        self.assertIn("docker", missing)
        self.assertNotIn("python", missing)


if __name__ == "__main__":
    unittest.main()
