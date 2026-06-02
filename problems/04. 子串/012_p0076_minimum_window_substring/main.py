import sys


def solve(data: str) -> str:
    lines = data.splitlines()
    if len(lines) < 2:
        return ""

    s = lines[0].strip()
    t = lines[1].strip()
    if not s or not t or len(s) < len(t):
        return ""

    need: dict[str, int] = {}
    for ch in t:
        need[ch] = need.get(ch, 0) + 1

    required = len(need)
    formed = 0
    window: dict[str, int] = {}
    left = 0
    best_left = 0
    best_len = len(s) + 1

    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            formed += 1

        while formed == required:
            cur_len = right - left + 1
            if cur_len < best_len:
                best_len = cur_len
                best_left = left

            left_ch = s[left]
            window[left_ch] -= 1
            if left_ch in need and window[left_ch] < need[left_ch]:
                formed -= 1
            left += 1

    if best_len == len(s) + 1:
        return ""

    return s[best_left : best_left + best_len]


def main() -> None:
    data = sys.stdin.read()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
