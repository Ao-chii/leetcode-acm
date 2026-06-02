import sys
from collections import defaultdict

def main() -> None:
    nums = list(map(int, input().split()))
    k = int(input())
    ans = 0
    s = [0] * (len(nums) + 1)

    for i, x in enumerate(nums):
        s[i + 1] = s[i] + x

    cnt = defaultdict(int)
    
    for j in s:
        ans += cnt[j - k]
        cnt[j] += 1

    print(ans)  


if __name__ == "__main__":
    main()
