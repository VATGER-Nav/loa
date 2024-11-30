import os
import toml
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
