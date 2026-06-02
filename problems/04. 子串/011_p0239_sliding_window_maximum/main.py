import sys
from collections import deque

def main() -> None:
    nums = list(map(int, input().split()))
    k = int(input())
    q = deque() # 记录窗口元素的下标

    for i, num in enumerate(nums):
        while q and nums[q[-1]] <= num:
            q.pop()
        q.append(i)

        if q[0] <= i - k:
            q.popleft()

        if i >= k - 1:
            print(nums[q[0]], end=" ")


if __name__ == "__main__":
    main()
