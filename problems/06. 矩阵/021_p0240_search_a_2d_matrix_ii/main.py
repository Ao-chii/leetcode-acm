import sys

def main() -> None:
    matrix = eval(input())
    m, n = len(matrix), len(matrix[0])
    target = int(input())

    i, j = 0, n - 1
    while i < m and j >= 0:
        if matrix[i][j] == target:
            print(True)
            return
        elif matrix[i][j] > target:
            j -= 1
        else:
            i += 1

    print(False)


if __name__ == "__main__":
    main()
