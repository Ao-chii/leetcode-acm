import sys

def main() -> None:
    height = list(map(int, input().split()))
    ans = 0
    left = 0
    right = len(height) - 1
    while left < right:
        ans = max(ans, min(height[left], height[right]) * (right - left))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    print(ans)


if __name__ == "__main__":
    main()
