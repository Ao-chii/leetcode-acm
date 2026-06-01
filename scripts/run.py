import argparse
import difflib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from study_plan import PROBLEMS_DIR, find_problem_dir, runnable_problem_dirs

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Example:
    name: str
    input_text: str
    output_text: str


def normalize_output(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def existing_problem_dirs(problem_name: str | None) -> list[Path]:
    if problem_name:
        problem_dir = find_problem_dir(problem_name)
        if problem_dir is None:
            raise SystemExit(f"problem not found: {problem_name}")
        return [problem_dir]

    if not PROBLEMS_DIR.is_dir():
        return []

    return runnable_problem_dirs()


def parse_examples(path: Path) -> list[Example]:
    if not path.is_file():
        return []

    lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    starts = [
        index
        for index, line in enumerate(lines)
        if line.strip().lower().startswith("example ") and line.strip().endswith(":")
    ]
    examples: list[Example] = []

    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        name = lines[start].strip().rstrip(":")
        block = lines[start + 1 : end]
        input_index = find_label(block, "Input:")
        output_index = find_label(block, "Output:")
        if input_index is None or output_index is None or input_index >= output_index:
            raise SystemExit(f"bad example format in {path}: {name}")

        input_text = "\n".join(block[input_index + 1 : output_index]).strip("\n")
        output_text = "\n".join(block[output_index + 1 :]).strip("\n")
        if input_text or output_text:
            examples.append(Example(name, input_text, output_text))

    return examples


def find_label(lines: list[str], label: str) -> int | None:
    for index, line in enumerate(lines):
        if line.strip() == label:
            return index
    return None


def show_diff(expected: str, actual: str) -> str:
    expected_lines = normalize_output(expected).splitlines()
    actual_lines = normalize_output(actual).splitlines()
    return "\n".join(
        difflib.unified_diff(
            expected_lines,
            actual_lines,
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )
    )


def run_example(problem_dir: Path, example: Example, timeout: float) -> bool:
    try:
        result = subprocess.run(
            [sys.executable, str(problem_dir / "main.py")],
            input=example.input_text,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        print(f"[FAIL] {problem_dir.name}/{example.name}: time limit exceeded")
        return False

    if result.returncode != 0:
        print(f"[FAIL] {problem_dir.name}/{example.name}: runtime error")
        print(result.stderr.rstrip())
        return False

    if normalize_output(result.stdout) != normalize_output(example.output_text):
        print(f"[FAIL] {problem_dir.name}/{example.name}: wrong answer")
        diff = show_diff(example.output_text, result.stdout)
        if diff:
            print(diff)
        return False

    print(f"[PASS] {problem_dir.name}/{example.name}")
    return True


def run_problem(problem_dir: Path, timeout: float, show_skip: bool) -> tuple[int, int]:
    examples = parse_examples(problem_dir / "examples.txt")
    if not examples:
        if show_skip:
            print(f"[SKIP] {problem_dir.name}: no examples")
        return 0, 0

    passed = 0
    for example in examples:
        if run_example(problem_dir, example, timeout):
            passed += 1
    return passed, len(examples)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("problem", nargs="?")
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()

    total_passed = 0
    total_examples = 0
    for problem_dir in existing_problem_dirs(args.problem):
        passed, examples = run_problem(problem_dir, args.timeout, args.problem is not None)
        total_passed += passed
        total_examples += examples

    if total_examples == 0:
        if args.problem is None:
            print("no local examples found")
        return

    print(f"{total_passed}/{total_examples} passed")
    if total_passed != total_examples:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
