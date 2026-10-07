import unittest

from casefoundry.generator import generate_suite
from casefoundry.parser import parse_requirements


PRD = """[R1] Upload text only.\n[R2] Ground every answer.\n[R3] Refuse unsupported answers.\n[R4] Admin deletes.\n[R5] Members cannot delete."""


class ParserGeneratorTests(unittest.TestCase):
    def test_parses_ids_and_text(self):
        requirements = parse_requirements(PRD)
        self.assertEqual([r.id for r in requirements], ["R1", "R2", "R3", "R4", "R5"])

    def test_rejects_duplicate_ids(self):
        with self.assertRaises(ValueError):
            parse_requirements("[R1] One\n[R1] Two")

    def test_rejects_missing_requirements(self):
        with self.assertRaises(ValueError):
            parse_requirements("# Nothing here")

    def test_generation_is_deterministic_and_traceable(self):
        requirements = parse_requirements(PRD)
        first = generate_suite(requirements)
        second = generate_suite(requirements)
        self.assertEqual(first, second)
        self.assertTrue(all(c.requirement_id.startswith("R") and c.evidence for c in first))

    def test_grid_has_hostile_and_boundary_cases(self):
        cases = generate_suite(parse_requirements(PRD))
        self.assertIn("hostile", {c.difficulty for c in cases})
        self.assertIn("boundary", {c.difficulty for c in cases})


if __name__ == "__main__":
    unittest.main()
