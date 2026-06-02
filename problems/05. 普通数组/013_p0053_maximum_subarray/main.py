import sys
from math import inf

def solve1() -> None:
    nums = list(map(int, input().split()))

    # f[i]表示以nums[i]结尾的最大子数组和
    f = [0] * len(nums)
    f[0] = nums[0]

    for i in range(1, len(nums)):
        f[i] = max(f[i - 1], 0) + nums[i]   

    print(max(f))
    
def solve2() -> None:
    nums = list(map(int, input().split()))
    ans = -inf
    f = 0
    for n in nums:
        f = max(f, 0) + n
        ans = max(ans, f)
    
    print(ans)

if __name__ == "__main__":
    solve2()
