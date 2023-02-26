# raz abergel
# Deja Vu exercise

def main():
    sum_of = 0
    number = input('Please enter a five digit number:\n')

    print("you entered the number :", int(number))

    print("the digits of this number : ", end="")
    for i in number[:-1]:
        print(int(i), ",", end="")
    print(number[4])

    print("the sum of the digits is : ", end="")
    for i in number:
        sum_of += int(i)
    print(sum_of)


if __name__ == "__main__":
    main()
