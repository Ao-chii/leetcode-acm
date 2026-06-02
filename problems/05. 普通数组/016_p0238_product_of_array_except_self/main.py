import sys

def method1() -> None:
    nums = list(map(int, input().split()))
    n = len(nums)

    pre = [1] * n
    suf = [1] * n

    for i in range(1, n):
        pre[i] = pre[i - 1] * nums[i - 1]

    for i in range(n - 2, -1, -1):
        suf[i] = suf[i + 1] * nums[i + 1]

    ans = []
    for i in range(n):
        ans.append(pre[i] * suf[i])

    print(ans)
    

def method2() -> None:
    nums = list(map(int, input().split()))
    n = len(nums)
    ans = [1] * n
    
    # 1. 计算左侧乘积，并直接存入 ans 数组
    # ans[i] 这里代表 nums[i] 左侧所有元素的乘积
    for i in range(1, n):
        ans[i] = nums[i - 1] * ans[i - 1]
        
    # 2. 动态计算右侧乘积，并与 ans[i] 里的左侧乘积相乘
    R = 1
    for i in range(n - 1, -1, -1):
        # 此时 ans[i] 原本存的是左侧乘积，乘以 R（右侧乘积）即为最终结果
        ans[i] *= R
        # 更新 R，将当前元素纳入右侧乘积中，供前一个元素使用
        R *= nums[i]
        
    print(ans)


if __name__ == "__main__":
    method2()
