import sys
from pathlib import Path

from study_plan import PROBLEMS_DIR, ROOT, find_problem_dir, plan_entries, planned_problem_dir


def ensure_inside_workspace(path: Path) -> Path:
    resolved = path.resolve()
    root = ROOT.resolve()
    if root != resolved and root not in resolved.parents:
        raise SystemExit(f"outside workspace: {resolved}")
    return resolved


def move_problem(group_name: str, order: int, problem: dict, dry_run: bool) -> bool:
    target = planned_problem_dir(problem)
    target_parent = target.parent
    current = find_problem_dir(f"p{int(problem['id']):04d}_{problem['slug'].replace('-', '_')}")

    if current is None:
        print(f"[MISS] {problem['id']} {problem['slug']}")
        return False

    if current.resolve() == target.resolve():
        print(f"[SKIP] {target.relative_to(ROOT)}")
        return False

    ensure_inside_workspace(current)
    ensure_inside_workspace(target_parent)
    if target.exists():
        raise SystemExit(f"target exists: {target.relative_to(ROOT)}")

    print(f"[MOVE] {current.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
    if not dry_run:
        target_parent.mkdir(parents=True, exist_ok=True)
        current.rename(target)
    return True


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    moved = 0
    for group_name, order, problem in plan_entries():
        if move_problem(group_name, order, problem, dry_run):
            moved += 1
    action = "would move" if dry_run else "moved"
    print(f"{action}: {moved}")

    if not dry_run:
        empty_groups = [path for path in PROBLEMS_DIR.iterdir() if path.is_dir() and not any(path.iterdir())]
        for path in empty_groups:
            path.rmdir()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
