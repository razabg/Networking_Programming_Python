# raz abergel
# Deja Vu exercise .

# the constant for the program
CORRECT_LEN = 5


def valid_input(num):
    """the function check the input whether It's valid or not
    the number must have 5 digit and no characters at all"""
    if num.isdigit():
        if len(num) == CORRECT_LEN:
            return False
        else:
            return True
    else:
        return True


def sum_digit(num):
    """the function sum the digits of the number"""
    sum_of = 0

    for i in num:
        sum_of += int(i)
    return sum_of


def split_num_to_digits(num):
    """the func split the number to digits and comma between every digit """
    list_of_digit = []
    for i in num[:-1]:
        list_of_digit.append(int(i))
        list_of_digit.append(",")
    list_of_digit.append(int(num[CORRECT_LEN-1]))

    return list_of_digit


def main():
    assert (valid_input("12345")) is False  # false means that the input is valid
    assert (valid_input("a")) is True  # true means that the input is invalid
    assert (valid_input("abcde")) is True
    assert (valid_input("abcd1")) is True
    assert (valid_input("123453525325235124")) is True
    assert sum_digit("12345") == 15
    assert sum_digit("55555") != 30
    assert split_num_to_digits("55555") == [5, ',', 5, ',', 5, ',', 5, ',', 5]

    number = input('Please enter a five digit number:\n')

    while valid_input(number) is True:
        print("you have entered invalid input ,try again\n")
        number = input("Please enter a five digit number:\n")

    print("you entered the number :", int(number))

    print("the digits of this number : ", end="")
    for i in split_num_to_digits(number):
        print(i, end="")

    print()
    print("the sum of the digits is : ", sum_digit(number))


"""main"""
if __name__ == "__main__":
    main()
