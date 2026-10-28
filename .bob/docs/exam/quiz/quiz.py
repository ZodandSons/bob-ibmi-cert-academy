#!/usr/bin/env python3
"""quiz.py - interactive practice quiz for IBM C3000-006 (IBM Bob v2 Developer - Associate).

Questions live in questions.yaml next to this script (original, weighted like the exam).

Usage:
  python3 quiz.py --exam                 all questions, shuffled (a full practice exam)
  python3 quiz.py --section 4            only section 4
  python3 quiz.py --objective 6.5        only one objective
  python3 quiz.py --count 15             random 15
  python3 quiz.py --review               print every question with answer and explanation
  python3 quiz.py --export-md FILE       write the question bank as Markdown
  python3 quiz.py --stats                show question counts per section and objective

Answer with option letters: "b" or, for "select two", "a,c" (any order, spaces allowed).
Type "q" to stop early and see your score. Needs PyYAML (pip install pyyaml).
"""
from __future__ import annotations

import argparse
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
BANK = HERE / "questions.yaml"
WEIGHTS = {1: 17, 2: 23, 3: 19, 4: 17, 5: 8, 6: 16}
LETTERS = "abcdefgh"


def load_bank() -> tuple[dict, list[dict]]:
    try:
        import yaml  # type: ignore
    except ImportError:
        sys.exit("PyYAML is required:  pip install pyyaml")
    data = yaml.safe_load(BANK.read_text(encoding="utf-8"))
    sections = {int(k): v for k, v in data["sections"].items()}
    questions = data["questions"]
    for q in questions:  # basic validation so a bad edit fails loudly
        missing = {"id", "section", "objective", "question", "options", "answer", "explain", "study"} - q.keys()
        if missing:
            sys.exit(f"Question {q.get('id', '?')} is missing fields: {', '.join(sorted(missing))}")
        if not set(q["answer"]) <= set(q["options"]):
            sys.exit(f"Question {q['id']}: answer {q['answer']} not among options {list(q['options'])}")
        q["section"] = int(q["section"])
        q["objective"] = str(q["objective"])
    return sections, questions


def shuffled_view(q: dict, rng: random.Random) -> tuple[list[tuple[str, str]], set[str]]:
    """Return options relabelled a, b, c... in a shuffled order, and the new correct letters."""
    items = list(q["options"].items())
    rng.shuffle(items)
    view, correct = [], set()
    for new_letter, (old_letter, text) in zip(LETTERS, items):
        view.append((new_letter, str(text)))
        if old_letter in q["answer"]:
            correct.add(new_letter)
    return view, correct


def select_two_hint(q: dict) -> str:
    n = len(q["answer"])
    return f"  (select {n})" if n > 1 and "select" not in q["question"].lower() else ""


def study_path(q: dict) -> str:
    return f".bob/docs/exam/{q['study']}"


def ask(q: dict, n: int, total: int, rng: random.Random) -> bool | None:
    view, correct = shuffled_view(q, rng)
    print(f"\n[{n}/{total}]  Section {q['section']} · Objective {q['objective']}  ({q['id']})")
    print(q["question"].strip() + select_two_hint(q))
    for letter, text in view:
        print(f"   {letter}) {text}")
    valid = {letter for letter, _ in view}
    while True:
        raw = input("Your answer: ").strip().lower()
        if raw in ("q", "quit", "exit"):
            return None
        picked = {p.strip() for p in raw.replace(" ", ",").split(",") if p.strip()}
        if picked and picked <= valid:
            break
        print(f"   Please type letter(s) from {', '.join(sorted(valid))}, e.g. b or a,c")
    ok = picked == correct
    print(("   ✅ Correct." if ok else f"   ❌ Not quite. Answer: {', '.join(sorted(correct))}"))
    print(f"   {q['explain'].strip()}")
    print(f"   Study: {study_path(q)}")
    return ok


def report(results: list[tuple[dict, bool]], sections: dict) -> None:
    if not results:
        print("\nNo questions answered.")
        return
    per = defaultdict(lambda: [0, 0])
    missed_obj = Counter()
    for q, ok in results:
        per[q["section"]][1] += 1
        if ok:
            per[q["section"]][0] += 1
        else:
            missed_obj[q["objective"]] += 1
    right = sum(ok for _, ok in results)
    print("\n" + "=" * 62)
    print(f"Score: {right}/{len(results)}  ({100 * right / len(results):.0f}%)")
    print("-" * 62)
    print(f"{'Section':<28}{'Weight':>8}{'Score':>10}{'%':>8}")
    weighted, weight_seen = 0.0, 0
    for s in sorted(per):
        r, t = per[s]
        pct = 100 * r / t
        weighted += pct * WEIGHTS[s]
        weight_seen += WEIGHTS[s]
        flag = "  ← review" if pct < 80 else ""
        print(f"{s} {sections[s]:<26}{WEIGHTS[s]:>7}%{r:>6}/{t:<3}{pct:>7.0f}%{flag}")
    print("-" * 62)
    print(f"Exam-weighted estimate: {weighted / weight_seen:.0f}%   (aim for ≥ 80% in every section)")
    if missed_obj:
        worst = ", ".join(f"{o} (×{c})" for o, c in missed_obj.most_common(6))
        print(f"Objectives to revisit: {worst}")
        print("See the objective map in .bob/docs/exam/README.md")


def export_md(questions: list[dict], sections: dict, out: Path) -> None:
    rng = random.Random(83)  # fixed seed chosen so correct answers spread evenly across a-d
    lines = [
        "# Practice questions: C3000-006 IBM Bob v2 Developer – Associate",
        "",
        "[Exam home](README.md) · Interactive version: `python3 .bob/docs/exam/quiz/quiz.py --exam`",
        "",
        f"{len(questions)} original questions, weighted like the exam. Each answer is hidden under",
        "\"Answer\". Try first, then expand. *Generated from `quiz/questions.yaml`; edit that file,",
        "then run `python3 quiz.py --export-md ../practice-questions.md`.*",
        "",
    ]
    for s in sorted(sections):
        qs = [q for q in questions if q["section"] == s]
        lines += [f"## Section {s} · {sections[s]} ({WEIGHTS[s]}%, {len(qs)} questions)", ""]
        for i, q in enumerate(qs, 1):
            view, correct = shuffled_view(q, rng)
            lines.append(f"**{q['id']}** · Objective {q['objective']}: {q['question'].strip()}{select_two_hint(q)}")
            lines.append("")
            for letter, text in view:
                lines.append(f"- {letter}) {text}")
            lines += [
                "",
                "<details><summary>Answer</summary>",
                "",
                f"**{', '.join(sorted(correct))}**. {q['explain'].strip()} [Study]({q['study']})",
                "",
                "</details>",
                "",
            ]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {out}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--exam", action="store_true", help="all questions, shuffled")
    g.add_argument("--section", type=int, choices=range(1, 7), metavar="1-6")
    g.add_argument("--objective", help="e.g. 4.2")
    g.add_argument("--review", action="store_true", help="print all questions with answers")
    g.add_argument("--export-md", type=Path, metavar="FILE")
    g.add_argument("--stats", action="store_true")
    ap.add_argument("--count", type=int, help="limit to N random questions")
    ap.add_argument("--seed", type=int, help="repeatable shuffle")
    args = ap.parse_args()

    sections, bank = load_bank()
    rng = random.Random(args.seed)

    if args.stats:
        by_sec = Counter(q["section"] for q in bank)
        print(f"{len(bank)} questions")
        for s in sorted(sections):
            objs = sorted({q['objective'] for q in bank if q['section'] == s}, key=lambda o: [int(x) for x in o.split('.')])
            print(f"  §{s} {sections[s]:<20} {by_sec[s]:>3} q ({100 * by_sec[s] / len(bank):.0f}% vs exam {WEIGHTS[s]}%)  objectives: {', '.join(objs)}")
        return 0
    if args.export_md:
        export_md(bank, sections, args.export_md)
        return 0
    if args.review:
        for q in bank:
            print(f"\n{q['id']} (§{q['section']} · {q['objective']}) {q['question'].strip()}")
            for k, v in q["options"].items():
                mark = "✔" if k in q["answer"] else " "
                print(f"  {mark} {k}) {v}")
            print(f"  → {q['explain'].strip()}\n  Study: {study_path(q)}")
        return 0

    pool = bank
    if args.section:
        pool = [q for q in bank if q["section"] == args.section]
    elif args.objective:
        pool = [q for q in bank if q["objective"] == args.objective]
        if not pool:
            sys.exit(f"No questions for objective {args.objective}. Try --stats.")
    pool = pool[:]
    rng.shuffle(pool)
    if args.count:
        pool = pool[: args.count]

    print(f"C3000-006 practice quiz: {len(pool)} question(s). Type q to stop.")
    results: list[tuple[dict, bool]] = []
    try:
        for i, q in enumerate(pool, 1):
            ok = ask(q, i, len(pool), rng)
            if ok is None:
                break
            results.append((q, ok))
    except (KeyboardInterrupt, EOFError):
        print()
    report(results, sections)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # e.g. piped into head
        sys.exit(0)
