import sys

NAME = 1


def main():
    print(sys.argv)
    print("Hello {}".format(sys.argv[NAME]))

    # OPEN FILE WITH AUTO' CLOSING (INSIDE THE CODE OF THE "WITH")
    # FILENAME = r'c:\networks\work\dear_prudence.txt'
    # with open(FILENAME, 'r') as input_file:
    #     for line in input_file:
    #         print(line, end="")

    # #append to file
    # input_file = open(r'c:\networks\work\dear_prudence.txt', 'a')
    # input_file.write('Dear Prudence open up your eyes\n')

    # read from file
    # input_file = open(r'c:\networks\works\dear_prudence.txt', 'r')
    # lyrics = None
    #
    # #  while lyrics != '':
    # #  lyrics = input_file.readline()
    # #   print(lyrics, end="")
    #
    # for line in input_file:
    #     print(line, end="")


"""main"""
if __name__ == "__main__":
    main()
