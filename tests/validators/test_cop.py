import unittest

from loa.validators.cop import validate_cop


class TestCopValidator(unittest.TestCase):
    def case_valid(self, cop: str, expected=None):
        output = validate_cop(cop)

        if expected:
            self.assertEqual(output, expected)

    def test_validate_cop(self):
        # valid:
        self.case_valid("BOT", "BOT")
        self.case_valid("DIXAT", "DIXAT")
        self.case_valid(" ELDAR ", "ELDAR")
