import tomllib
import unittest
from pathlib import Path

from loa import Agreement


class TestAgreement(unittest.TestCase):
    def get_default_agreement(self) -> Agreement:
        """returns an instance of Agreement which passes all validation"""
        return Agreement(from_sector="ed/DUS", to_sector="ed/BOT", ades=["EDDF"])

    def test_on_data(self):
        """all agreements should create a valid Agreement object"""

        for root, _, files in Path("data/").walk():
            for file in files:
                if not file.endswith(".toml") or file.endswith("docs.toml"):
                    continue

                file_path = root / file
                with file_path.open("rb") as toml_file:
                    data = tomllib.load(toml_file)

                    for element in data["agreements"]:
                        Agreement(**element)

    def test_adep_ades_validation(self):
        """Agreement must have ADEP or ADES set"""

        # model without ADEP and ADES should raise a ValueError
        with self.assertRaises(ValueError):
            Agreement(from_sector="ed/DUS", to_sector="ed/BOT")

        # model with ADEP or model with ADES set should not raise any errors
        Agreement(from_sector="ed/DUS", to_sector="ed/BOT", adep=["EDDF"])
        Agreement(from_sector="ed/DUS", to_sector="ed/BOT", ades=["EDDF"])

    def test_runway_validation(self):
        agreement = self.get_default_agreement()
        agreement.runway = ["05L"]
        agreement.runway = ["36", "05L"]
        agreement.runway = None

        with self.assertRaises(ValueError):
            agreement.runway = ["05P"]
