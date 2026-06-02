import sys
from collections import deque

def main() -> None:
    nums = list(map(int, input().split()))
    k = int(input())
    q = deque() # 记录窗口元素的下标
    ans = []
    for i, num in enumerate(nums):
        while q and nums[q[-1]] <= num:
            q.pop()
        q.append(i)

        if q[0] <= i - k:
            q.popleft()

        if i >= k - 1:
            ans.append(nums[q[0]])
    print(ans)
    
if __name__ == "__main__":
    main()
