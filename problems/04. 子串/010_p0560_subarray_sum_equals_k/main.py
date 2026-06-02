import sys
from collections import defaultdict

def main() -> None:
    nums = list(map(int, input().split()))
    k = int(input())
    s = [0] * (len(nums) + 1)
    for i, num in enumerate(nums):
        s[i + 1] = s[i] + num

    d = defaultdict(int)
    ans = 0
    for c in s:
        ans += d[c - k]
        d[c] += 1

    print(ans)

if __name__ == "__main__":
    main()
