import sys
from collections import defaultdict

def main() -> None:
    strs = input().split()
    d = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        d[key].append(s)
    
    print(list(d.values()))

if __name__ == "__main__":
    main()
