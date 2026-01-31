import sys

from loa.data import Data


def combine():
    data = Data()
    data.read_data()
    data.read_docs()
    data.combine_data()
    data.combine_docs()

    if len(Data().errors) > 0:
        print("Errors:")
        for error in Data().errors:
            print(error)
        sys.exit(1)


def check():
    data = Data()
    data.read_data()
    data.read_docs()

    if len(Data().errors) > 0:
        print("Errors:")
        for error in Data().errors:
            print(error)
        sys.exit(1)
