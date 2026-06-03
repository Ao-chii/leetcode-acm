import sys

def main() -> None:
    matrix = eval(input())
    n = len(matrix)

    # 先转置
    for i in range(n):
        for j in range(i):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # 再水平翻转
    for i in range(n):
        matrix[i].reverse()
    print(matrix)


if __name__ == "__main__":
    main()
