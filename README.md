# Claude Skills

Two [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
for Claude that make working with AI agents safer and more honest: a security
auditor for skill packages, and a debugging-integrity guard.

Each skill is a self-contained folder — a `SKILL.md` of instructions Claude
loads on demand, plus Python helper scripts and a test suite.

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

## Installing

Both skills need Python 3.12+ for their helper scripts.

```bash
git clone https://github.com/Himanshu040604/Claude-Skills.git
cp -r Claude-Skills/skill-security-audit ~/.claude/skills/
cp -r Claude-Skills/skeptical-debugger  ~/.claude/skills/
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
└── skeptical-debugger/
    ├── SKILL.md
    ├── scripts/      parse_diff.py · detect_cheats.py · cheat_patterns.json
    ├── references/   gaming-vs-legitimate.md
    └── tests/        pytest suite + fixtures
```

## Running the tests

From either skill's directory:

```bash
uv run --with pytest pytest tests/ -v
```

`skill-security-audit` has 11 tests; `skeptical-debugger` has 18.

## License

MIT — see [LICENSE](LICENSE).

## Author

Himanshu Singh — [@Himanshu040604](https://github.com/Himanshu040604)
