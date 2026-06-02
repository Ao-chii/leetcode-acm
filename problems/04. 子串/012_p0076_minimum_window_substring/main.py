import sys
from collections import Counter

def main() -> None:
    s = input()
    t = input()
    m = 0
    n = len(s)
    ans = ""
    
    sc = Counter()
    tc = Counter(t)

    if len(s) < len(t):
        return
    
    if s == t:
        print(s)
        return

    for right, c in enumerate(s):
        sc[c] += 1
        while sc >= tc:
            if right - m + 1 <= n:
                n = right - m + 1
                ans = s[m:right + 1]
            sc[s[m]] -= 1
            m += 1
    
    print(ans)

if __name__ == "__main__":
    main()
