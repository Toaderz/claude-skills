#!/usr/bin/env python3
"""Repo-specific lint for capabilities under plugins/.

Covers what `claude plugin validate --strict` does not: reserved words in skill
names, description length, body length, relative-link resolution, duplicate
content, registry consistency, and a static trigger-coverage matrix.

Every check here is deterministic, local, and free. Nothing in this file makes a
network call or invokes a paid service. See docs/architecture.md for the cost
policy and for what these checks cannot establish.

Exit codes: 0 = clean, 1 = errors found.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PLUGINS = REPO / "plugins"
SCENARIOS = Path(__file__).with_name("scenarios.json")
REGISTRY = REPO / "registry" / "registry.json"

RESERVED_WORDS = ("claude", "anthropic")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_BODY_LINES = 500

# Markdown links are genuine links and must resolve. Paths mentioned in inline
# code are usually prose describing a structure to *produce* (see the ICM
# templates), so they are reported separately rather than failed.
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
INLINE_PATH_RE = re.compile(r"`([^`\n]{2,120}?)`")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
PATH_SUFFIXES = (".md", ".json", ".py", ".sh", ".yaml", ".yml", ".txt")

errors: list[str] = []
warnings: list[str] = []
notes: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def note(msg: str) -> None:
    notes.append(msg)


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)


def strip_fences(text: str) -> str:
    """Drop fenced code blocks so illustrative trees are not scanned for links."""
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def parse_frontmatter(path: Path) -> tuple[dict, str] | tuple[None, str]:
    """Minimal YAML frontmatter reader. Handles scalars, >- and | blocks, and
    inline lists — enough for skill and agent frontmatter, without a dependency."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, text

    data: dict[str, str] = {}
    key: str | None = None
    buf: list[str] = []

    def flush() -> None:
        if key is not None:
            data[key] = "\n".join(buf).strip() if buf else data.get(key, "")

    for raw in lines[1:end]:
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if m and not raw.startswith((" ", "\t", "-")):
            flush()
            key, rest = m.group(1), m.group(2).strip()
            if rest in (">", "|", ">-", "|-", ">+", "|+"):
                buf = []
            else:
                data[key] = rest.strip("\"'")
                buf = []
                key = key if rest in ("", ">", "|") else None
                if key is not None:
                    buf = []
        elif key is not None:
            buf.append(raw.strip())
    flush()
    return data, "\n".join(lines[end + 1 :])


# ---------------------------------------------------------------- skills


def check_skill(path: Path) -> dict | None:
    fm, body = parse_frontmatter(path)
    if fm is None:
        err(f"{rel(path)}: no YAML frontmatter — this skill can never be discovered")
        return None

    name = fm.get("name", "").strip()
    desc = fm.get("description", "").strip()

    if not name:
        err(f"{rel(path)}: frontmatter has no `name`")
    else:
        if len(name) > MAX_NAME:
            err(f"{rel(path)}: name is {len(name)} chars (max {MAX_NAME})")
        if not NAME_RE.match(name):
            err(f"{rel(path)}: name '{name}' is not lowercase kebab-case")
        for word in RESERVED_WORDS:
            if word in name.lower():
                err(f"{rel(path)}: name '{name}' contains reserved word '{word}'")
        expected = path.parent.name
        if name != expected:
            err(f"{rel(path)}: name '{name}' does not match its directory '{expected}'")

    if not desc:
        err(f"{rel(path)}: frontmatter has no `description` — nothing to route on")
    elif len(desc) > MAX_DESCRIPTION:
        err(f"{rel(path)}: description is {len(desc)} chars (max {MAX_DESCRIPTION})")

    body_lines = len(body.strip().split("\n"))
    if body_lines > MAX_BODY_LINES:
        err(f"{rel(path)}: body is {body_lines} lines (max {MAX_BODY_LINES})")

    return {"path": path, "name": name, "description": desc, "lines": body_lines}


def check_agent(path: Path) -> None:
    fm, _ = parse_frontmatter(path)
    if fm is None:
        err(f"{rel(path)}: agent has no YAML frontmatter")
        return
    if not fm.get("name"):
        err(f"{rel(path)}: agent has no `name`")
    if not fm.get("description"):
        err(f"{rel(path)}: agent has no `description` — it can never be delegated to")
    if "tools" not in fm:
        warn(
            f"{rel(path)}: agent declares no `tools`; it inherits everything. "
            "Bounded tools are required by docs/capability-policy.md"
        )


# ---------------------------------------------------------------- links


def check_links(md_files: list[Path]) -> None:
    unresolved_mentions = 0
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        prose = strip_fences(text)
        base = path.parent

        for target in MD_LINK_RE.findall(prose):
            target = target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if "${" in target:  # ${CLAUDE_PLUGIN_ROOT} and friends resolve at runtime
                continue
            resolved = (base / target).resolve()
            if not resolved.exists():
                err(f"{rel(path)}: broken link -> {target}")

        for mention in INLINE_PATH_RE.findall(prose):
            mention = mention.strip()
            if not mention.endswith(PATH_SUFFIXES) or " " in mention:
                continue
            if mention.startswith(("http", "/", "~", "$", "npx ", "claude ")):
                continue
            if any(c in mention for c in "<>*{}"):  # placeholder patterns
                continue
            if not (base / mention).exists() and not (REPO / mention).exists():
                unresolved_mentions += 1
    if unresolved_mentions:
        note(
            f"{unresolved_mentions} inline-code path mention(s) across the repo do not resolve. "
            "These are not failed: prose paths usually describe structure to produce, not files "
            "that ship. Review them if a skill claims to read one."
        )


# ---------------------------------------------------------------- duplicates


def check_duplicates(files: list[Path]) -> None:
    # Eval graders legitimately repeat identical one-line assertions across cases —
    # "preflight-planning fired" means the same thing wherever it is asserted. Only
    # capability content is checked for accidental duplication.
    files = [f for f in files if "/evals/" not in f.as_posix()]
    by_hash: dict[str, list[Path]] = {}
    for f in files:
        h = hashlib.md5(f.read_bytes()).hexdigest()
        by_hash.setdefault(h, []).append(f)
    for paths in by_hash.values():
        if len(paths) > 1:
            err("duplicate content: " + " == ".join(rel(p) for p in paths))

    synced = Path.home() / ".claude" / "skills" / "synced"
    if not synced.is_dir():
        return
    repo_hashes = {hashlib.md5(f.read_bytes()).hexdigest(): f for f in files}
    hits = []
    for s in synced.rglob("*.md"):
        h = hashlib.md5(s.read_bytes()).hexdigest()
        if h in repo_hashes:
            hits.append(f"{rel(repo_hashes[h])} == ~/{s.relative_to(Path.home())}")
    if hits:
        warn(
            "identical to account-synced skills (double-load risk; removing the account copy "
            "needs the claude.ai UI):\n      " + "\n      ".join(hits)
        )


# ---------------------------------------------------------------- registry


def check_registry(skills: list[dict]) -> None:
    if not REGISTRY.exists():
        note("registry/registry.json not present yet — consistency check skipped")
        return
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"registry/registry.json is not valid JSON: {e}")
        return

    entries = data.get("capabilities", [])

    for e in entries:
        name, path = e.get("name"), e.get("path")
        if path and not (REPO / path).exists():
            err(f"registry: '{name}' points at missing path {path}")
        for field in ("name", "type", "plugin", "path", "purpose", "scope", "status"):
            if not e.get(field):
                err(f"registry: '{name or '?'}' is missing required field '{field}'")

    registered_skills = {e.get("name") for e in entries if e.get("type") == "skill"}
    on_disk = {s["name"] for s in skills}

    for orphan in sorted(registered_skills - on_disk):
        err(f"registry: skill '{orphan}' is registered but does not exist on disk")
    for missing in sorted(on_disk - registered_skills):
        err(f"registry: skill '{missing}' exists on disk but is not registered")


# ---------------------------------------------------------------- coverage


# A description's "do NOT use" clause is what buys precision. Terms appearing there
# mean the skill explicitly disclaims the scenario — the opposite of competing for it.
NEGATIVE_CLAUSE_RE = re.compile(
    # Spanish puts a clitic between the negation and the verb ("NO la uses para..."),
    # which a literal "no uses" misses — and missing it counts an excluded term as a
    # positive claim, which is exactly backwards.
    r"\b(do not use|don't use|do not trigger|never use|not for"
    r"|no(?: l[ao]s?)? uses|nunca(?: l[ao]s?)? uses|no la actives|no actives)\b",
    re.I,
)


def split_description(desc: str) -> tuple[str, str]:
    """Return (positive claim, exclusion clause) of a skill description.

    Line breaks inside a YAML folded scalar are arbitrary wrapping, so they are
    collapsed first: without this, an exclusion clause that happens to wrap mid-phrase
    ("no la\n  uses para...") is never recognised, and every term it disclaims is
    counted as a positive claim instead.
    """
    desc = " ".join(desc.split())
    m = NEGATIVE_CLAUSE_RE.search(desc)
    return (desc, "") if not m else (desc[: m.start()], desc[m.start() :])


def check_trigger_coverage(skills: list[dict]) -> None:
    if not SCENARIOS.exists():
        note("scripts/lib/scenarios.json not found — coverage matrix skipped")
        return
    scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))["scenarios"]

    split = {s["name"]: split_description(s["description"].lower()) for s in skills}

    def hits(term: str, text: str) -> bool:
        # Word-boundary match, so "trivial" does not fire inside "non-trivial".
        return re.search(rf"(?<![\w-]){re.escape(term)}(?![\w-])", text) is not None

    print("\n  Static trigger-coverage matrix (lexical proxy — NOT proof of routing)")
    print("  " + "-" * 72)
    for sc in scenarios:
        terms = [t.lower() for t in sc["terms"]]
        # Score = how many DISTINCT scenario terms a description claims. A skill that
        # matches one generic verb ("refactor") is not competing with one that matches
        # six; counting membership instead of strength was flagging healthy separation
        # as a precision failure.
        score = {n: sum(hits(t, pos) for t in terms) for n, (pos, _) in split.items()}
        matched = sorted((n for n, k in score.items() if k), key=lambda n: -score[n])
        excluded = [n for n, (_, neg) in split.items() if any(hits(t, neg) for t in terms)]
        # A scenario may legitimately want more than one skill: "plan it out, then
        # check the work when it's done" is two requests in one sentence.
        raw = sc.get("expect", "")
        expects = [raw] if isinstance(raw, str) else list(raw)
        expects = [e for e in expects if e and e != "none"]
        expect = expects[0] if expects else ("none" if raw == "none" else "")
        shown = ", ".join(f"{n}({score[n]})" for n in matched) or "(none)"

        if expect == "none":
            status = "ok  " if not matched else "WARN"
            if matched:
                warn(
                    f"scenario '{sc['id']}' expects no repo skill to compete, but "
                    f"{', '.join(matched)} claim it. {sc.get('note', '')}"
                )
            elif excluded:
                note(
                    f"scenario '{sc['id']}': explicitly excluded by "
                    f"{', '.join(excluded)} — the exclusion clause is doing its job"
                )
        elif expects and any(e not in matched for e in expects):
            status = "GAP "
            available = {s["name"] for s in skills}
            for e in (e for e in expects if e not in matched):
                if e in available:
                    warn(
                        f"scenario '{sc['id']}': expected skill '{e}' exists but its "
                        "description does not contain any scenario term — likely recall failure"
                    )
                else:
                    note(f"scenario '{sc['id']}': expected skill '{e}' not built yet")
        else:
            # Precision risk is a rival claiming the scenario at least as strongly as
            # the skill that is supposed to own it — not merely a rival existing.
            # One shared generic verb ("build", "review") is noise, not competition:
            # a rival needs at least two scenario terms before this proxy claims
            # anything. Every rival is still printed, whatever its score.
            floor = max(2, min((score.get(e, 0) for e in expects), default=0))
            rivals = [n for n in matched if n not in expects and score[n] >= floor]
            if rivals:
                status = "WARN"
                warn(
                    f"scenario '{sc['id']}': {', '.join(rivals)} match as strongly as "
                    f"{' + '.join(expects)} — precision risk"
                )
            else:
                status = "ok  "
        print(f"  {status} {sc['id']:<20} -> {shown}")


# ---------------------------------------------------------------- legacy


def check_unmigrated() -> None:
    legacy = []
    for p in REPO.iterdir():
        if p.name.startswith(".") or p.name in {
            "plugins", "docs", "scripts", "registry", "integrations",
            "README.md", "CLAUDE.md", "LICENSE",
        }:
            continue
        if p.is_dir() and any(p.rglob("SKILL.md")):
            legacy.append(rel(p))
        elif p.is_file() and p.suffix in (".md", ".skill"):
            legacy.append(rel(p))
    if legacy:
        note(
            f"{len(legacy)} capability path(s) still outside plugins/ (pre-migration): "
            + ", ".join(sorted(legacy))
        )


# ---------------------------------------------------------------- main


def main() -> int:
    if not PLUGINS.is_dir():
        print("no plugins/ directory yet — nothing to lint")
        return 0

    skill_files = sorted(PLUGINS.glob("*/skills/*/SKILL.md"))
    agent_files = sorted(PLUGINS.glob("*/agents/*.md"))
    md_files = sorted(PLUGINS.rglob("*.md"))

    # Link checking covers the WHOLE repository, not just plugins/. Restricting it to
    # plugins/ left the root CLAUDE.md, README, docs/ and integrations/ unchecked — and
    # that is precisely where a link rots, because deleting a capability directory does
    # not touch the documents that point at it. The cleanup commit left six dead paths
    # in CLAUDE.md and this checker reported a clean run.
    all_md = sorted(
        f
        for f in REPO.rglob("*.md")
        if ".git" not in f.parts and "node_modules" not in f.parts
    )

    skills = [s for s in (check_skill(f) for f in skill_files) if s]
    for f in agent_files:
        check_agent(f)

    check_links(all_md)
    check_duplicates(md_files)
    check_registry(skills)
    check_trigger_coverage(skills)
    check_unmigrated()

    print(f"\n  {len(skills)} skill(s), {len(agent_files)} agent(s), {len(all_md)} markdown file(s) linted")

    for label, items in (("NOTE", notes), ("WARN", warnings), ("ERROR", errors)):
        for item in items:
            print(f"  {label}: {item}")

    if errors:
        print(f"\n  FAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\n  PASS — 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
