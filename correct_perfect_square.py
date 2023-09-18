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

    sq_root = math.sqrt(input_num)

    matrix = [[0 for _ in range(int(sq_root))] for _ in range(int(sq_root))]
    num = 1

    for i in range(int(sq_root)):
        for j in range(int(sq_root)):
            matrix[i][j] = num
            num += 1
    return matrix


if __name__ == "__main__":
    while True:
        n = int(input("Enter number-"))
        result = generate_matrix(n)
        if isinstance(result, list):
            print(result)
            break
        print(result)
