import sys
from collections import Counter


def solve(data: str) -> str:
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return ""
    if len(lines) == 1:
        parts = lines[0].split()
        if len(parts) < 2:
            return ""
        s, t = parts[0], parts[1]
    else:
        s, t = lines[0], lines[1]

    need = Counter(t)
    missing = len(t)
    left = 0
    best_start = 0
    best_len = len(s) + 1

    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1

        while missing == 0:
            window_len = right - left + 1
            if window_len < best_len:
                best_len = window_len
                best_start = left

            left_ch = s[left]
            need[left_ch] += 1
            if need[left_ch] > 0:
                missing += 1
            left += 1

    if best_len > len(s):
        return ""
    return s[best_start : best_start + best_len]


def main() -> None:
    data = sys.stdin.read()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
