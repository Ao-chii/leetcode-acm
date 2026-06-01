import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from study_plan import PROBLEMS_DIR, ROOT, hot100_by_slug, planned_problem_dir

DATA_PATH = ROOT / "data" / "hot100.json"

ENDPOINTS = {
    "cn": "https://leetcode.cn/graphql/",
    "com": "https://leetcode.com/graphql",
}

QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    title
    translatedTitle
    titleSlug
    difficulty
    content
    translatedContent
    exampleTestcases
    codeSnippets {
      lang
      langSlug
      code
    }
  }
}
"""


def problem_dir(problem_id: int, slug: str) -> Path:
    known = hot100_by_slug().get(slug)
    if known:
        return planned_problem_dir(known)
    return PROBLEMS_DIR / f"p{problem_id:04d}_{slug.replace('-', '_')}"


def strip_tags(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
    value = re.sub(r"</p\s*>", "\n\n", value, flags=re.IGNORECASE)
    value = re.sub(r"<li\s*>", "- ", value, flags=re.IGNORECASE)
    value = re.sub(r"</li\s*>", "\n", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value)


def html_to_markdown(content: str) -> str:
    if not content:
        return ""

    pre_blocks: list[str] = []

    def replace_pre(match: re.Match) -> str:
        text = strip_tags(match.group(1)).strip()
        pre_blocks.append(f"\n```text\n{text}\n```\n")
        return f"\n@@PRE_BLOCK_{len(pre_blocks) - 1}@@\n"

    content = re.sub(r"<pre[^>]*>(.*?)</pre>", replace_pre, content, flags=re.DOTALL | re.IGNORECASE)
    text = strip_tags(content)
    for index, block in enumerate(pre_blocks):
        text = text.replace(f"@@PRE_BLOCK_{index}@@", block)

    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def pick_python_snippet(question: dict) -> str:
    snippets = question.get("codeSnippets") or []
    for lang_slug in ("python3", "python"):
        for snippet in snippets:
            if snippet.get("langSlug") == lang_slug:
                return snippet.get("code", "")
    return ""


def fetch_question(slug: str, site: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"titleSlug": slug}}).encode("utf-8")
    endpoint = ENDPOINTS[site]
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Origin": endpoint.removesuffix("/graphql").removesuffix("/graphql/"),
            "Referer": f"{endpoint.removesuffix('/graphql').removesuffix('/graphql/')}/problems/{slug}/",
            "User-Agent": "leetcode-hot100-local-fetcher",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if payload.get("errors"):
        raise RuntimeError(payload["errors"])

    question = payload.get("data", {}).get("question")
    if not question:
        raise RuntimeError(f"question not found: {slug}")
    return question


def save_question(question: dict, fallback_problem: dict | None, keep_raw: bool) -> Path:
    fallback_id = fallback_problem["id"] if fallback_problem else None
    question_id = int(question.get("questionFrontendId") or fallback_id or question["questionId"])
    slug = question["titleSlug"]
    title = question.get("translatedTitle") or question["title"]
    target_dir = problem_dir(question_id, slug)
    target_dir.mkdir(parents=True, exist_ok=True)

    content = question.get("translatedContent") or question.get("content") or ""
    statement = (
        f"# {question_id}. {title}\n\n"
        f"Difficulty: `{question.get('difficulty', '')}`\n\n"
        f"Slug: `{slug}`\n\n"
        f"{html_to_markdown(content)}"
    )
    (target_dir / "statement.md").write_text(statement, encoding="utf-8")

    if keep_raw:
        (target_dir / "examples.raw.txt").write_text(question.get("exampleTestcases") or "", encoding="utf-8")
        snippet = pick_python_snippet(question)
        if snippet:
            (target_dir / "leetcode.py").write_text(snippet + "\n", encoding="utf-8")

    return target_dir


def slugs_from_args(args: argparse.Namespace) -> list[str]:
    problems = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if args.all:
        return [problem["slug"] for problem in problems]
    if args.slug:
        return args.slug
    raise SystemExit("provide slug(s) or --all")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", nargs="*")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--site", choices=sorted(ENDPOINTS), default="cn")
    parser.add_argument("--keep-raw", action="store_true")
    args = parser.parse_args()

    known = hot100_by_slug()
    ok = 0
    failed = 0
    for slug in slugs_from_args(args):
        try:
            question = fetch_question(slug, args.site)
            target_dir = save_question(question, known.get(slug), args.keep_raw)
            print(f"[OK] {slug} -> {target_dir.relative_to(ROOT)}")
            ok += 1
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError) as exc:
            print(f"[FAIL] {slug}: {exc}")
            failed += 1

    print(f"fetched: {ok}, failed: {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
