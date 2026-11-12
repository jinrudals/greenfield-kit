#!/usr/bin/env python3
"""Check that a docs/greenfield/ artifact tree is internally consistent.

Usage: check_artifacts.py <root> [<root> ...]  (exit 1 on any problem)
Zero dependencies.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skills import parse_frontmatter  # noqa: E402

ITEM_RE = re.compile(r"^- \*\*(?P<id>[^*]+)\*\*\s*(?:\[(?P<status>[^\]]*)\])?(?P<rest>.*)$")
ID_RES = {
    "vision": re.compile(r"^V-\d+$"),
    "roadmap": re.compile(r"^R-M\d+-\d+$"),
    "todo": re.compile(r"^T-M\d+-\d+$"),
}
ADR_RE = re.compile(r"^(ADR-\d{3})(?:-|$)")
ANY_ID_RE = re.compile(r"\b(?:V-\d+|R-M\d+-\d+|T-M\d+-\d+|ADR-\d{3})\b")
REF_RE = re.compile(r"\b(?:refs|deps):\s*([^;(]*)")
STATUSES = {"pending", "in_progress", "done", "dropped"}


def _kind(rel):
    if rel.parts[0] == "adr":
        return "adr"
    if rel.parts[0] == "todo":
        return "todo"
    return rel.stem


def _inputs(fm):
    raw = fm.get("inputs", "").strip().strip("[]")
    return [p.strip() for p in raw.split(",") if p.strip()]


def check(root):
    root = Path(root)
    if not root.is_dir():
        return [f"{root}: not a directory"]
    if not any(root.rglob("*.md")):
        return [f"{root}: no Markdown documents found"]
    errors = []
    docs = {}  # key (path without .md) -> dict(rel, kind, fm)
    items = {}  # id -> (rel, kind, status)
    adrs = {}  # ADR id -> fm
    pending_refs = []  # (rel, item id, status, ref id)

    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        rels = rel.as_posix()
        kind = _kind(rel)
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{rels}: missing or malformed frontmatter")
            continue
        if kind == "adr":
            m = ADR_RE.match(rel.stem)
            if not m:
                errors.append(f"{rels}: ADR file name must start with ADR-<nnn> (three digits)")
                continue
            if m.group(1) in adrs:
                errors.append(f"{rels}: duplicate ADR number {m.group(1)}")
            if fm.get("status") not in ("accepted", "superseded"):
                errors.append(f"{rels}: `status` must be accepted or superseded")
            adrs[m.group(1)] = (rels, fm)
            continue
        if not re.fullmatch(r"\d+", fm.get("version", "")):
            errors.append(f"{rels}: `version` must be an integer")
        if fm.get("status") not in ("draft", "approved"):
            errors.append(f"{rels}: `status` must be draft or approved")
        docs[rel.with_suffix("").as_posix()] = {"rel": rels, "fm": fm}

        seen = set()
        for line in text.lstrip("\ufeff").splitlines():
            m = ITEM_RE.match(line)
            if not m:
                continue
            item_id, status, rest = m.group("id"), m.group("status"), m.group("rest")
            pattern = ID_RES.get(kind)
            if pattern is not None and not pattern.match(item_id):
                errors.append(f"{rels}: {item_id}: malformed item ID for {kind}")
                continue
            if item_id in seen or item_id in items:
                errors.append(f"{rels}: duplicate item ID {item_id}")
            seen.add(item_id)
            if status is not None and status not in STATUSES:
                errors.append(f"{rels}: {item_id}: unknown status [{status}]")
            if status == "dropped" and "(reason:" not in rest:
                errors.append(f"{rels}: {item_id}: dropped item needs (reason: ...)")
            items[item_id] = (rels, kind, status)
            for m in REF_RE.finditer(rest):
                ids = ANY_ID_RE.findall(m.group(1))
                if not ids:
                    errors.append(f"{rels}: {item_id}: refs/deps has no valid ID")
                for ref in ids:
                    pending_refs.append((rels, kind, item_id, status, ref))

    known = set(items) | set(adrs)
    for rels, kind, item_id, status, ref in pending_refs:
        if ref not in known:
            errors.append(f"{rels}: {item_id} references unknown ID {ref}")
        elif kind == "todo" and status != "dropped" and items.get(ref, (None, None, None))[2] == "dropped":
            errors.append(f"{rels}: {item_id} references dropped item {ref} but is not dropped")

    for key, info in docs.items():
        if info["fm"].get("status") != "approved":
            continue
        for dep in _inputs(info["fm"]):
            target = docs.get(dep)
            if target is None:
                errors.append(f"{info['rel']}: input {dep} is missing")
            elif target["fm"].get("status") != "approved":
                errors.append(f"{info['rel']}: input {dep} is not approved")

    for adr_id, (rels, fm) in adrs.items():
        if fm.get("status") != "superseded":
            continue
        target = fm.get("superseded_by", "")
        if not target:
            errors.append(f"{rels}: {adr_id} is superseded but has no superseded_by")
        elif target not in adrs:
            errors.append(f"{rels}: {adr_id} superseded_by {target} which does not exist")

    for start in adrs:
        seen, cur = set(), start
        while cur in adrs and adrs[cur][1].get("status") == "superseded":
            if cur in seen:
                errors.append(f"{adrs[start][0]}: supersede cycle involving {start}")
                break
            seen.add(cur)
            cur = adrs[cur][1].get("superseded_by", "")
    return list(dict.fromkeys(errors))


def main(argv):
    if len(argv) < 2:
        print("usage: check_artifacts.py <root> [<root> ...]", file=sys.stderr)
        return 2
    total = 0
    for arg in argv[1:]:
        for err in check(Path(arg)):
            print(f"::error::{arg}: {err}")
            total += 1
    print(f"{total} problem(s) found")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
