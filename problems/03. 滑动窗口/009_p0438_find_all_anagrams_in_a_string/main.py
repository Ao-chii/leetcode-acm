import sys
from collections import Counter

def main() -> None:
    s = input()
    p = input()
    sc = Counter()
    pc = Counter(p)

    ans = []

    for right in range(len(s)):
        sc[s[right]] += 1
        if right >= len(p):
            sc[s[right - len(p)]] -= 1
            #if sc[s[right - len(p)]] == 0:
            #    del sc[s[right - len(p)]]

        if sc == pc:
            ans.append(right - len(p) + 1)

    print(ans)

if __name__ == "__main__":
    main()
