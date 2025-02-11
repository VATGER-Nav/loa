from classes.data import Data


if __name__ == "__main__":
    data = Data()
    data.read_data()
    data.combine_data()

    for error in data.errors:
        print(error)
