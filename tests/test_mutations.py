import unittest

from casefoundry.generator import generate_suite
from casefoundry.mutations import MUTATIONS, mutation_score, toy_app
from casefoundry.parser import parse_requirements


PRD = "\n".join(["[R1] Upload policy", "[R2] Ground answers", "[R3] Refuse unsupported", "[R4] Admin deletes", "[R5] Member cannot delete"])


class MutationTests(unittest.TestCase):
    def test_baseline_policy(self):
        self.assertEqual(toy_app({"action": "upload", "extension": "exe", "size": 1}), "deny")
        self.assertEqual(toy_app({"action": "delete", "role": "administrator"}), "allow")

    def test_mutations_change_behavior(self):
        self.assertEqual(toy_app({"action": "answer", "has_source": False}, "unsupported_answered"), "grounded")

    def test_generated_suite_kills_all_seeded_mutations(self):
        report = mutation_score(generate_suite(parse_requirements(PRD)))
        self.assertEqual(report.total, len(MUTATIONS))
        self.assertEqual(report.score, 1.0)
        self.assertEqual(report.survivors, ())

    def test_happy_path_only_is_inadequate(self):
        cases = [c for c in generate_suite(parse_requirements(PRD)) if c.difficulty == "happy"]
        self.assertLess(mutation_score(cases).score, 1.0)


if __name__ == "__main__":
    unittest.main()
