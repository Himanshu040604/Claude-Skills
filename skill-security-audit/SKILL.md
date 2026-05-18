---
name: skill-security-audit
description: Audits a single Claude skill package (SKILL.md plus bundled scripts) for malicious or unsafe content before it is installed or trusted. Use when the user shares a skill via a GitHub/marketplace URL or local folder, asks to install or add a skill, or explicitly asks to audit, vet, or security-check a skill.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Skill Security Audit

Audits one Claude skill package and returns a verdict: safe / review needed / block.
**Static analysis only — NEVER execute the audited skill or run its scripts.**

## Trigger Detection

Activate when the user:
- Shares a skill via a GitHub/marketplace URL or a local skill folder
- Asks to install, add, or try a skill
- Explicitly asks to audit, vet, or security-check a skill

## Audit Pipeline

### 1. Acquire
- URL: create a temp dir with `mktemp -d /tmp/skill-audit-XXXXXX`, then
  `git clone --depth 1 <url> <tempdir>`.
- Local path: use it directly, read-only.
- Never copy the package into `~/.claude/skills/`.
- If acquisition fails, remove any temp dir already created, then report the
  failure and stop.

### 2. Inventory
List every file (`Glob`, `ls -la`). Flag binaries, hidden files, archives, and
executables. If there is no `SKILL.md` at the package root, report "not a valid
skill package" and stop — emit no verdict.

### 3. Mechanical Scan
Run: `python3 ~/.claude/skills/skill-security-audit/scripts/scan_patterns.py <path>`
Parse the JSON output (findings list + severity summary).

### 4. Semantic Review
Read `~/.claude/skills/skill-security-audit/references/threat-checklist.md` and
apply Part 2: review the `SKILL.md`
prose, the `description`, the `allowed-tools` declaration, and each script for
malicious *intent* that regex cannot catch.

### 5. Verdict
A mechanical scan hit is a signal, not a proof. Apply the rubric only to
findings that **survive Step 4 semantic review** — a mechanical hit that
Step 4 judged a false positive (e.g. prose that merely *describes* a danger
pattern, with no malicious intent) is dismissed and does NOT count toward the
verdict. Merge the surviving mechanical findings with the semantic findings,
then apply the rubric to that merged set:
- BLOCK — any surviving CRITICAL finding.
- REVIEW NEEDED — any surviving HIGH or MEDIUM finding.
- SAFE — only LOW/INFO findings survive, or none.

### 6. Report & Cleanup
Print the report (format below). Delete any temp dir created in step 1.

## Report Format

    # Skill Security Audit — <skill name>

    Verdict: <SAFE | REVIEW NEEDED | BLOCK>
    Inventory: <N files> (<flagged items, if any>)

    | Severity | Category | Location | Detail |
    |----------|----------|----------|--------|
    | ...      | ...      | file:line| ...    |

    Reasoning: <why this verdict>
    Recommended action: <install / review specific items / do not install>

State explicitly when there are no findings, and return SAFE.
