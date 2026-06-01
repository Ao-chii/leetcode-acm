import sys
from collections import defaultdict

def main() -> None:
    s = input()
    d = defaultdict(int)
    ans = 0
    left = 0
    for right in range(len(s)):
        d[s[right]] += 1
        while d[s[right]] > 1:
            d[s[left]] -= 1
            left += 1
        ans = max(ans, right - left + 1)

    print(ans)

if __name__ == "__main__":
    main()
