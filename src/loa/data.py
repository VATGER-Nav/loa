import json
import tomllib
from pathlib import Path

from pydantic import ValidationError

from .agreement import Agreement


class Data:
    _instance = None
    data: list[Agreement]
    errors: list[str]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "data_dir"):  # Prevent re-initialization
            self.data_dir = Path("data")
            self.output_dir = Path("dist")
            self.data = []
            self.errors = []

            self.count_read = 0

    def read_data(self):
        if not self.data_dir.exists():
            msg = f"Directory {self.data_dir} does not exist"
            raise FileNotFoundError(msg)

        for root, _, files in self.data_dir.walk():
            if root == self.data_dir:
                continue

            for file in files:
                if not file.endswith(".toml"):
                    continue

                file_path = root / file
                self.read_toml(file_path)

        print(f"Read {self.count_read} agreements, {len(self.errors)} errors")

    def read_toml(self, file_path: Path):
        print(file_path)
        try:
            with file_path.open("rb") as toml_file:
                data = tomllib.load(toml_file)

                for aggrement_dict in data["agreements"]:
                    try:
                        self.count_read += 1
                        self.data.append(Agreement(**aggrement_dict))
                    except ValidationError as e:
                        self.errors.append(f"Failed on {file_path} with {e}")

        except (tomllib.TOMLDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Exception {e}. Failed on {file_path}")

    def combine_data(self):
        output_file = self.output_dir / "agreements.json"

        self.output_dir.mkdir(parents=True, exist_ok=True)

        agreements_list = [agreement.model_dump() for agreement in self.data]

        json_data = {"agreements": agreements_list}

        with output_file.open("w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file)

        print(f"Combined data written to {output_file}")
