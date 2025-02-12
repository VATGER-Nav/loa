from .agreement import Agreement
from .data import Data

__all__ = ["Agreement", "Data"]

import sys


def combine():
    data = Data()
    data.read_data()
    data.combine_data()

    if len(Data().errors) > 0:
        print("Errors:")
        for error in Data().errors:
            print(error)
        sys.exit(1)


def check():
    Data().read_data()

    if len(Data().errors) > 0:
        print("Errors:")
        for error in Data().errors:
            print(error)
        sys.exit(1)
