import sys

def main() -> None:
    height = list(map(int, input().split()))
    left, right = 0, len(height) - 1
    lm = rm = 0
    ans = 0

    while left < right:
        lm = max(lm, height[left])
        rm = max(rm, height[right])
        if height[left] < height[right]:
            ans += lm - height[left]
            left += 1
        else:
            ans += rm - height[right]
            right -= 1

    print(ans)


if __name__ == "__main__":
    main()
