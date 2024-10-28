
import sys
import argparse

def main():
    try:
        parser = argparse.ArgumentParser(
                        prog='read_generator',
                        description='Reads files too large for ram',
                        epilog='end of program')
        parser.add_argument('input file', type =csvname)
        args = parser.parse_args()
        file = args.input
    except argparse.ArgumentTypeError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

        # TO TEST AGAINST
    # create_huge_file()
    # open_no_generator(file)  # This will take a long time to open

    # Median of the ecaluated moves depth run in the engine for each move
    median_depth = 0
    open_file(file)
    for i in open_file(file):
        x = i.split(",")
        if x[2].isdigit():
            median_depth += int(x[2]) 
            median_depth = median_depth/2
            print(median_depth)
    

   
def csvname(inn):
    if not inn.endswith('.csv'):
        raise argparse.ArgumentTypeError("File must be a .csv file")
    return inn

def open_file(file):
    with open(file, "r") as f: # opens and auto closes file
        for line in f:
            yield line

# def create_huge_file():
#     with open("large_file.txt", "w") as f:
#         for i in range(500000000):  # Adjust the number for a larger file
#             f.write(f"This is line {i}\n")



# def open_no_generator(file):
#     lines =[]
#     with open(file, "r") as f:
#         for i in open_file(file):
#             lines+=i
#     return lines

if __name__ == "__main__":
    main()