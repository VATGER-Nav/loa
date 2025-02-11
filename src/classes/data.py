import os
import tomllib
import toml
from pydantic import ValidationError

from views.agreement import Agreement


class Data:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Data, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "data_dir"):  # Prevent re-initialization
            self.data_dir = "data/"
            self.output_dir = "api/"
            self.data = []
            self.errors = []

            self.count_read = 0

    def read_data(self):
        if not os.path.exists(self.data_dir):
            raise FileNotFoundError(f"Directory {self.data_dir} does not exist")

        for root, _, files in os.walk(self.data_dir):
            if root == self.data_dir:
                continue

            for file in files:
                if not file.endswith(".toml"):
                    continue

                file_path = os.path.join(root, file)
                self.read_toml(file_path)

        print(f"Read {self.count_read} agreements, {len(self.errors)} errors")

    def read_toml(self, file_path):
        print(file_path)
        try:
            with open(file_path, "rb") as toml_file:

                data = tomllib.load(toml_file)

                for aggrement_dict in data["agreements"]:
                    try:
                        self.count_read += 1
                        self.data.append(Agreement.from_dict(aggrement_dict))
                    except ValidationError as e:
                        self.errors.append(f"Failed on {file_path} with {e}")

        except (tomllib.TOMLDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Exception {e}. Failed on {file_path}")

    def combine_data(self):
        output_file = os.path.join(self.output_dir, "agreements.toml")

        os.makedirs(self.output_dir, exist_ok=True)

        agreements_list = [agreement.model_dump() for agreement in self.data]

        toml_data = {"agreements": agreements_list}

        with open(output_file, "w", encoding="utf-8") as toml_file:
            toml.dump(toml_data, toml_file)

        print(f"Combined data written to {output_file}")
