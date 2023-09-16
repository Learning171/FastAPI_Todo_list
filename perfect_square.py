import math


def perfect_square(func):
    def inner(input_num):
        if math.isqrt(input_num) ** 2 == input_num:
            return func(input_num)
        else:
            return "it is not perfect square number, please enter perfect square number"

    return inner


@perfect_square
def generate_matrix(input_num):
    if input_num <= 0:
        return "input number must be perfect square"

    matrix = [[0 for _ in range(input_num)] for _ in range(input_num)]
    num = 1

    for i in range(input_num):
        for j in range(input_num):
            matrix[i][j] = num
            num += 1
    return matrix


if __name__ == "__main__":
    while True:
        n = int(input("Enter number-"))
        result = generate_matrix(n)

        if isinstance(result, list):
            for row in result:
                print(row)

        else:
            print(result)
