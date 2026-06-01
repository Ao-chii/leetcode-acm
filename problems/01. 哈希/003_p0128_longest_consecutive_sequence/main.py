import sys

def main() -> None:
    nums = list(map(int, input().split()))
    s = set(nums)
    ans = 0
    for n in s:
        if n - 1 not in s:
            length = 1
            while n + length in s:
                length += 1
            ans = max(ans, length)
        continue

if __name__ == "__main__":
    main()
