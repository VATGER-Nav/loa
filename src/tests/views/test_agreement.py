import os
import tomllib
import unittest
from views.agreement import Agreement


class TestAgreement(unittest.TestCase):
    def test_on_data(self):
        """all agreements should create a valid Agreement object"""

        data_dir = "data/"
        for root, _, files in os.walk(data_dir):
            for file in files:
                if not file.endswith(".toml"):
                    continue

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as toml_file:
                        data = tomllib.load(toml_file)

                        for element in data["agreements"]:
                            Agreement.from_dict(element)

                except Exception as e:
                    self.fail(f"Exception {e}. Failed on {file_path}")

    def test_adep_ades_validation(self):
        """Agreement must have ADEP or ADES set"""

        # model without ADEP and ADES should raise a ValueError
        with self.assertRaises(ValueError):
            Agreement(from_sector="ed/DUS", to_sector="ed/BOT")

        # ADEP and ADES must be of type list
        with self.assertRaises(ValueError):
            Agreement(from_sector="ed/DUS", to_sector="ed/BOT", adep="EDDF")
        with self.assertRaises(ValueError):
            Agreement(from_sector="ed/DUS", to_sector="ed/BOT", ades="EDDF")

        # model with ADEP or model with ADES set should not raise any errors
        Agreement(from_sector="ed/DUS", to_sector="ed/BOT", adep=["EDDF"])
        Agreement(from_sector="ed/DUS", to_sector="ed/BOT", ades=["EDDF"])

    def test_runway_validation(self):
        Agreement(
            from_sector="ed/DUS", to_sector="ed/BOT", ades=["EDDF"], runway=["05L"]
        )
        Agreement(
            from_sector="ed/DUS",
            to_sector="ed/BOT",
            ades=["EDDF"],
            runway=["36", "05L"],
        )

        with self.assertRaises(ValueError):
            Agreement(
                from_sector="ed/DUS", to_sector="ed/BOT", ades=["EDDF"], runway=["05P"]
            )
