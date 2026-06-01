import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBLEMS_DIR = ROOT / "problems"


MAIN_TEMPLATE = '''import sys


def solve(data: str) -> str:
    return ""


def main() -> None:
    data = sys.stdin.read()
    sys.stdout.write(solve(data))


if __name__ == "__main__":
    main()
'''


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def create_problem(number: int, title: str) -> Path:
    slug = slugify(title)
    if not slug:
        raise SystemExit("empty title")

    problem_dir = PROBLEMS_DIR / f"p{number:04d}_{slug}"
    if problem_dir.exists():
        raise SystemExit(f"already exists: {problem_dir}")

    problem_dir.mkdir(parents=True)
    (problem_dir / "main.py").write_text(MAIN_TEMPLATE, encoding="utf-8")
    return problem_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int)
    parser.add_argument("title", nargs="+")
    args = parser.parse_args()

    problem_dir = create_problem(args.number, " ".join(args.title))
    print(problem_dir.relative_to(ROOT))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
