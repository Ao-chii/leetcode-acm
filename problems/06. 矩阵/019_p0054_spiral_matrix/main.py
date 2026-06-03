import sys

def main() -> None:
    matrix = eval(input())

    if not matrix:
        print([])
        return
    
    l, r = 0, len(matrix[0]) - 1
    u, d = 0, len(matrix) - 1

    ans = []

    while True:
        for i in range(l, r + 1):
            ans.append(matrix[u][i])
        u += 1

        if u > d:
            break

        for i in range(u, d + 1):
            ans.append(matrix[i][r])
        r -= 1

        if l > r:
            break

        for i in range(r, l - 1, -1):
            ans.append(matrix[d][i])
        d -= 1

        if u > d:
            break

        for i in range(d, u - 1, -1):
            ans.append(matrix[i][l])
        l += 1

        if l > r:
            break

    print(ans)


if __name__ == "__main__":
    main()
