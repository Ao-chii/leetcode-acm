import sys

def main() -> None:
    intervals = eval(input())
    intervals.sort(key=lambda x: x[0])
    ans = []

    for i in intervals:
        if ans and i[0] <= ans[-1][1]:
            ans[-1][1] = max(ans[-1][1], i[1])
        else:
            ans.append(i)
    
    print(ans)

if __name__ == "__main__":
    main()
