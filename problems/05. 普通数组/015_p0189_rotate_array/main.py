import sys

nums = list(map(int, input().split()))
k = int(input())

def method1(nums: list[int], k: int) -> None:
    n = len(nums)
    k %= n
    if k % n == 0:
        return
    
    nums[:] = nums[-k:] + nums[:-k]

def method2(nums: list[int], k: int) -> None:
    n = len(nums)
    k %= n
    
    def reverse(start: int, end: int) -> None:
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1
            
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)


if __name__ == "__main__":
    method2(nums, k)
