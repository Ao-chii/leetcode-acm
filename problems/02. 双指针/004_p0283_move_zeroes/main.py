import sys

def main() -> None:
    nums = list(map(int, input().split()))
    left = 0
    for i in range(len(nums)):
        if nums[i]:
            nums[left], nums[i] = nums[i], nums[left]
            left += 1
    print(nums)

if __name__ == "__main__":
    main()
