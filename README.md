# leetcode-hot100

ACM mode practice workspace for LeetCode Hot 100.

## Layout

```text
data/
  hot100.json
problems/
  p0001_two_sum/
    main.py
    examples.txt
    statement.md
    leetcode.py
    examples.raw.txt
scripts/
  import_hot100.py
  fetch_leetcode.py
  new_problem.py
  run.py
notes/
  hot100.md
```

Only `main.py` is the training target. It reads stdin and writes stdout.

## Example Format

Use one `examples.txt` per problem:

```text
Example 1:
Input:
3 3
2 1 1
1 1 0
0 1 1
Output:
4
```

Add more cases by appending `Example 2:`, `Example 3:`, and so on.

## Run Examples

Run one problem:

```powershell
python scripts/run.py p0001_two_sum
```

Run every problem that has runnable examples:

```powershell
python scripts/run.py
```

## Add Problems

Create one custom problem:

```powershell
python scripts/new_problem.py 49 group-anagrams
```

Create the Hot 100 skeleton:

```powershell
python scripts/import_hot100.py
```

Fetch statement, raw LeetCode examples, and the Python `Solution` template:

```powershell
python scripts/fetch_leetcode.py two-sum
python scripts/fetch_leetcode.py --all
```

The fetch script does not convert LeetCode examples into ACM examples. LeetCode has function-call examples, not a real stdin contract. Write `examples.txt` yourself so the local format stays honest.

## Main File Contract

```python
import sys


def solve(data: str) -> str:
    return ""


def main() -> None:
    data = sys.stdin.read()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
```

Keep the entry ACM-style. Put algorithm logic in helper functions if needed.
