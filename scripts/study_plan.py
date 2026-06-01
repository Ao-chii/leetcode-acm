import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
HOT100_PATH = DATA_DIR / "hot100.json"
STUDY_PLAN_PATH = DATA_DIR / "study_plan.json"
PROBLEMS_DIR = ROOT / "problems"


def load_hot100() -> list[dict]:
    return json.loads(HOT100_PATH.read_text(encoding="utf-8"))


def load_study_plan() -> list[dict]:
    return json.loads(STUDY_PLAN_PATH.read_text(encoding="utf-8"))


def hot100_by_id() -> dict[int, dict]:
    return {int(problem["id"]): problem for problem in load_hot100()}


def hot100_by_slug() -> dict[str, dict]:
    return {problem["slug"]: problem for problem in load_hot100()}


def problem_dir_name(problem: dict, order: int | None = None) -> str:
    slug = problem["slug"].replace("-", "_")
    base = f"p{int(problem['id']):04d}_{slug}"
    return f"{order:03d}_{base}" if order is not None else base


def plan_entries() -> list[tuple[str, int, dict]]:
    problems = hot100_by_id()
    entries: list[tuple[str, int, dict]] = []
    global_order = 1
    for group in load_study_plan():
        for problem_id in group["problems"]:
            entries.append((group["name"], global_order, problems[int(problem_id)]))
            global_order += 1
    return entries


def planned_problem_dir(problem: dict) -> Path:
    problem_id = int(problem["id"])
    for group_name, order, planned_problem in plan_entries():
        if int(planned_problem["id"]) == problem_id:
            return PROBLEMS_DIR / group_name / problem_dir_name(problem, order)
    return PROBLEMS_DIR / problem_dir_name(problem)


def find_problem_dir(problem_name: str) -> Path | None:
    direct = PROBLEMS_DIR / problem_name
    if direct.is_dir():
        return direct

    matches = [
        path
        for path in PROBLEMS_DIR.rglob("*")
        if path.is_dir()
        and (path.name == problem_name or path.name.endswith(f"_{problem_name}"))
        and (path / "main.py").is_file()
    ]
    return sorted(matches)[0] if matches else None


def runnable_problem_dirs() -> list[Path]:
    return sorted(
        path
        for path in PROBLEMS_DIR.rglob("*")
        if path.is_dir() and (path / "main.py").is_file()
    )
