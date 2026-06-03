import sys

def method1() -> None:
    matrix = eval(input())

    row_has_zero = [0 in row for row in matrix]  # 行是否包含 0
    col_has_zero = [0 in col for col in zip(*matrix)]  # 列是否包含 0

    for i, row0 in enumerate(row_has_zero):
        for j, col0 in enumerate(col_has_zero):
            if row0 or col0:  # i 行或 j 列有 0
                matrix[i][j] = 0  # 题目要求原地修改，无返回值
    
    print(matrix)


def method2() -> None:
    matrix = eval(input())
    m, n = len(matrix), len(matrix[0])
    f1, f2 = 0 in matrix[0], 0 in (matrix[i][0] for i in range(m))

    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = matrix[0][j] = 0
    
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
                
    if f1:
        for j in range(n):
            matrix[0][j] = 0
    if f2:
        for i in range(m):
            matrix[i][0] = 0

if __name__ == "__main__":
    method1()
