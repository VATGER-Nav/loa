import sys
from classes.data import Data


if __name__ == "__main__":
    Data().read_data()

    if len(Data().errors) > 0:
        print("Errors:")
        for error in Data().errors:
            print(error)
        sys.exit(1)
