import argparse


def parse_file(file_path):
    with open(file_path, "r") as file:
        header = file.readline()

        for line in file:
            print(line, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Music recommendation application")
    parser.add_argument("file_path", type=str, help="Input file path for table")
    #  parser.add_argument('-f','--file_path', type=str, help='Input file path for table')
    args = parser.parse_args()

    # print(args.file_path)

    parse_file(args.file_path)
