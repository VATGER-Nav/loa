import unittest

from loa.validators.runway import validate_runway


class TestRunwayValidator(unittest.TestCase):
    def case_invalid(self, runway: str):
        with self.assertRaises(ValueError):
            validate_runway(runway)

    def case_valid(self, runway: str, expected=None):
        output = validate_runway(runway)

        if expected:
            self.assertEqual(output, expected)

    def test_validate_runway(self):
        # valid:
        self.case_valid("01", "01")
        self.case_valid("36", "36")

        self.case_valid("01C", "01C")
        self.case_valid("36C", "36C")
        self.case_valid("01L", "01L")
        self.case_valid("36L", "36L")
        self.case_valid("01R", "01R")
        self.case_valid("36R", "36R")

        self.case_valid(" 36R ", "36R")

        # invalid:
        self.case_invalid("1")
        self.case_invalid("37")
        self.case_invalid("31P")
        self.case_invalid("011")
        self.case_invalid("ABL")

    def test_validate_runways(self):
        valid_runways = ["01", "18", "36", "01C", "36C", "18L", "27R", " 20L "]
        for runway in valid_runways:
            self.case_valid(runway)

        invalid_runways = ["", "1", "37", "37", "31P", "011", "ABL"]
        for runway in invalid_runways:
            self.case_invalid(runway)
