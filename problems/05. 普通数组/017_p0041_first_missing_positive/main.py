import sys

def main() -> None:
    nums = list(map(int, input().split()))
    n = len(nums)

    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[j], nums[i] = nums[i], nums[j]
        
    for i in range(n):
        if nums[i] - 1 != i:
            print(i + 1)
            return

    print(n + 1)
    
if __name__ == "__main__":
    main()
