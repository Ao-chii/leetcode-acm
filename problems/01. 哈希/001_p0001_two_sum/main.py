import sys

def main() -> None:
    nums = list(map(int, input().split()))
    target = int(input())
    num_dict = {}
    for i, num in enumerate(nums):
        j = target - num
        if j in num_dict:
            print(num_dict[j], i)
            return
        num_dict[num] = i
        
if __name__ == "__main__":
    main()
