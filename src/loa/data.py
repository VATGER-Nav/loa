import json
import tomllib
from pathlib import Path
from shutil import copy

from pydantic import ValidationError

from .agreement import Agreement
from .doc import Doc


class Data:
    _instance = None
    data: list[Agreement]
    docs: list[Doc]
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
            self.docs = []
            self.errors = []

            self.count_read = 0
            self.docs_read = 0

    def read_data(self):
        if not self.data_dir.exists():
            msg = f"Directory {self.data_dir} does not exist"
            raise FileNotFoundError(msg)

        for root, _, files in self.data_dir.walk():
            if root == self.data_dir:
                continue

            for file in files:
                if not file.endswith(".toml") or file.endswith("docs.toml"):
                    continue

                file_path = root / file
                self.read_toml(file_path)

        print(f"Read {self.count_read} agreements, {len(self.errors)} errors")

    def read_docs(self):
        docs_path = self.data_dir / "_docs" / "docs.toml"
        if not docs_path.exists():
            msg = f"Document index {docs_path} does not exist"
            raise FileNotFoundError(msg)

        try:
            with docs_path.open("rb") as toml_file:
                data = tomllib.load(toml_file)

                for doc_dict in data["docs"]:
                    try:
                        self.docs_read += 1
                        doc = Doc(**doc_dict)

                        if not (self.data_dir / "_docs" / doc.filename).exists():
                            msg = f"Missing doc referenced: {doc.filename}"
                            raise FileNotFoundError(msg)

                        self.docs.append(doc)
                    except ValidationError as e:
                        self.errors.append(f"Failed on {docs_path} with {e}")
        except (tomllib.TOMLDecodeError, FileNotFoundError, PermissionError) as e:
            print(f"Exception {e}. Failed on {docs_path}")

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

    def combine_docs(self):
        output_file = self.output_dir / "docs.json"

        self.output_dir.mkdir(parents=True, exist_ok=True)

        docs_list = [doc.model_dump() for doc in self.docs]

        json_data = {"docs": docs_list}

        with output_file.open("w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file)

        doc_dir = self.output_dir / "docs"
        doc_dir.mkdir(parents=True, exist_ok=True)

        for doc in self.docs:
            copy(self.data_dir / "_docs" / doc.filename, doc_dir / doc.filename)

        print(f"Combined doc data written to {output_file}")
