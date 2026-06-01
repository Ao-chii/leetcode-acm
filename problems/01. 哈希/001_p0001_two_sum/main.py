import sys


def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        need = target - num
        if need in seen:
            return seen[need], i
        seen[num] = i
    return -1, -1


def solve(data: str) -> str:
    tokens = list(map(int, data.split()))
    if not tokens:
        return ""

    n, target = tokens[0], tokens[1]
    nums = tokens[2 : 2 + n]
    i, j = two_sum(nums, target)
    return f"{i} {j}"


def main() -> None:
    data = sys.stdin.read()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
