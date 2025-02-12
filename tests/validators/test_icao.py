import unittest

from loa.validators.icao import validate_icao, validate_icaos


class TestIcaoValidator(unittest.TestCase):
    def case_validate_icao_valid(self, icao, expected=None):
        output = validate_icao(icao)

        if expected:
            self.assertEqual(output, expected)

    def case_validate_icao_invalid(self, icao):
        with self.assertRaises(ValueError):
            validate_icao(icao)

    def test_validate_icao(self):
        # valid icaos:
        self.case_validate_icao_valid("eddf", expected="EDDF")
        self.case_validate_icao_valid("EDDF", expected="EDDF")
        self.case_validate_icao_valid("eddm", expected="EDDM")
        self.case_validate_icao_valid("EDDM", expected="EDDM")
        self.case_validate_icao_valid("EDDM", expected="EDDM")

        # invalid icaos:
        self.case_validate_icao_invalid("EDDGG")
        self.case_validate_icao_invalid("EDDG1")
        self.case_validate_icao_invalid("eddm1")

    def test_validate_icaos(self):
        # valid icaos:
        icaos = ["EDDF", "eddf", "EDDM", "EDCQ ", " EDMA"]
        validated_icaos = validate_icaos(icaos)

        self.assertEqual(len(icaos), len(validated_icaos))

        for icao, validated_icao in zip(icaos, validated_icaos, strict=True):
            self.assertEqual(validated_icao, validate_icao(icao))
