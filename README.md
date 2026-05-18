# Claude Skills

Three [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
for Claude Code: a security auditor for skill packages, a debugging-integrity
guard, and a guide for producing rich HTML artifacts instead of flat markdown.

Each skill is a self-contained folder — a `SKILL.md` of instructions Claude
loads on demand, plus any helper scripts, references, or assets it needs.

## Skills

### `skill-security-audit`

Audits a Claude skill package for malicious or unsafe content **before you
install it**. An untrusted skill is both a prompt-injection surface (its
`SKILL.md` enters Claude's context) and a code-execution surface (its scripts
run with your privileges) — this vets one first.

- **Mechanical scan** — applies a 23-pattern catalog (dangerous shell,
  obfuscation, credential exfiltration, suspicious network calls, prompt
  injection, unicode tricks) to every file.
- **Semantic review** — Claude then reads the prose and scripts for malicious
  *intent* that pattern-matching can't catch.
- **Verdict** — ✅ safe · ⚠️ review needed · 🛑 block.

Activates when you share a skill by URL or local path, or ask to audit one.

### 🔍 `skeptical-debugger`

A debugging-integrity layer. A green test means nothing if the test was gamed —
this skill bans the shortcuts used to fake a passing checkmark: patching the
test to pass, skipping or deleting a failing test, weakening assertions,
swallowing exceptions, or claiming "fixed" without proof.

- **Integrity protocol** — reproduce → hypothesize → fix the *root cause* →
  re-run the *original, unmodified* check.
- **Cheat-detector** — inspects the debugging session's diff and flags gaming
  patterns (skip markers, removed assertions, swallowed errors, deleted tests).
- **Verdict gate** — a fix is accepted only when the real check passes and the
  detector is clean, or every flag is justified in writing.

Complements the `systematic-debugging` skill — it adds the integrity
guardrails, it doesn't replace the process.

### `html-artifacts`

Helps Claude recognize when an **HTML artifact** is a better deliverable than
a markdown file — a long spec, a plan, a code/PR review, a research report, or
a one-off editing/triage interface — and how to make one that's genuinely
useful. It is *not* "always emit HTML": short answers and diff-reviewed docs
stay markdown.

- **Decision** — a clear test for when HTML beats markdown (length, tables,
  diffs, diagrams, interactivity, sharing) and when to stay in markdown.
- **Five playbooks** — specs/planning, code review, design/prototypes,
  reports/research, and custom editing interfaces, each with example prompts.
- **Starter skeleton** — a self-contained, responsive `starter.html` (tabs,
  code blocks, SVG, an export button) to adapt instead of starting blank.

Distilled from Thariq Shihipar's "The Unreasonable Effectiveness of HTML."

## Installing

`skill-security-audit` and `skeptical-debugger` need Python 3.12+ for their
helper scripts; `html-artifacts` has none.

```bash
git clone https://github.com/Himanshu040604/Claude-Skills.git
cp -r Claude-Skills/skill-security-audit ~/.claude/skills/
cp -r Claude-Skills/skeptical-debugger  ~/.claude/skills/
cp -r Claude-Skills/html-artifacts      ~/.claude/skills/
```

Claude Code discovers skills in `~/.claude/skills/` automatically.

## Repository layout

```
Claude-Skills/
├── skill-security-audit/
│   ├── SKILL.md
│   ├── scripts/      scan_patterns.py · fileio.py · patterns.json
│   ├── references/   threat-checklist.md
│   └── tests/        pytest suite + fixtures
├── skeptical-debugger/
│   ├── SKILL.md
│   ├── scripts/      parse_diff.py · detect_cheats.py · cheat_patterns.json
│   ├── references/   gaming-vs-legitimate.md
│   └── tests/        pytest suite + fixtures
└── html-artifacts/
    ├── SKILL.md
    ├── references/   use-case-playbooks.md
    └── assets/       starter.html
```

## Running the tests

From `skill-security-audit/` or `skeptical-debugger/`:

```bash
uv run --with pytest pytest tests/ -v
```

`skill-security-audit` has 11 tests; `skeptical-debugger` has 18.

## License

MIT — see [LICENSE](LICENSE).

## Author

Himanshu Singh — [@Himanshu040604](https://github.com/Himanshu040604)
