import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "hot100.json"
PROBLEMS_DIR = ROOT / "problems"


MAIN_TEMPLATE = '''import sys


def solve(data: str) -> str:
    tokens = data.split()
    if not tokens:
        return ""
    return ""


def main() -> None:
    data = sys.stdin.read()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
'''


EXAMPLES_TEMPLATE = """Example 1:
Input:

Output:
"""


def problem_dir_name(problem: dict) -> str:
    slug = problem["slug"].replace("-", "_")
    return f"p{problem['id']:04d}_{slug}"


def load_hot100() -> list[dict]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def create_problem(problem: dict, dry_run: bool) -> bool:
    problem_dir = PROBLEMS_DIR / problem_dir_name(problem)
    if problem_dir.exists():
        print(f"[SKIP] {problem_dir.relative_to(ROOT)}")
        return False

    print(f"[CREATE] {problem_dir.relative_to(ROOT)}")
    if dry_run:
        return True

    problem_dir.mkdir(parents=True)
    (problem_dir / "main.py").write_text(MAIN_TEMPLATE, encoding="utf-8")
    (problem_dir / "examples.txt").write_text(EXAMPLES_TEMPLATE, encoding="utf-8")
    (problem_dir / "statement.md").write_text(
        f"# {problem['id']}. {problem['title']}\n\nSlug: `{problem['slug']}`\n",
        encoding="utf-8",
    )
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    problems = load_hot100()
    if args.limit is not None:
        problems = problems[: args.limit]

    created = sum(1 for problem in problems if create_problem(problem, args.dry_run))
    action = "would create" if args.dry_run else "created"
    print(f"{action}: {created}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
