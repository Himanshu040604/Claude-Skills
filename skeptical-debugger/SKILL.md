---
name: skeptical-debugger
description: Enforces debugging integrity when fixing a bug, a test failure, or unexpected behavior, and before declaring a fix done. Use whenever debugging or fixing failing tests. It bans gaming the test or signal and checks the fix is real. Pairs with the systematic-debugging skill.
---

# Skeptical Debugger

The integrity layer for debugging. A passing check means nothing if you made the
check lie. This skill governs what you may NOT do while fixing a bug, and checks
that a claimed fix is real.

**For the root-cause investigation *process*, use the `systematic-debugging`
skill. This skill adds the integrity guardrails on top of it.**

## When to Use

Whenever you are debugging a bug, a test failure, or unexpected behavior — and
especially before you declare a fix "done".

## The Iron Law

```
A FIX IS REAL ONLY WHEN THE ORIGINAL, UNMODIFIED FAILING CHECK PASSES
FOR THE RIGHT REASON. MAKING THE SIGNAL LIE IS NOT A FIX.
```

## Banned Actions

NEVER do any of these to make a failure "go away":
- Patch the test so it passes.
- Patch application code only to satisfy a test, without fixing the bug.
- Skip, delete, xfail, or .only-isolate a failing test.
- Weaken or delete an assertion.
- Mock or stub the failure away.
- Swallow the exception (`except: pass`, empty `catch {}`, `# type: ignore`).
- Hardcode the expected value.
- Claim "fixed" without showing the check actually pass.

## The Protocol

1. **Reproduce** — run the failing check; watch it fail before changing anything.
2. **Hypothesize** — state the root cause. Use the `systematic-debugging` skill
   for the investigation process.
3. **Fix the root cause** — in source code, not in the test and not in the signal.
4. **Re-run the original, unmodified check** — it must pass, for the predicted
   reason.
5. **Run the cheat-detector** (below) on the session's diff.
6. **Justify or revert** — every flagged change is justified in writing or
   reverted. Show the real command output as proof.

## Running the Cheat-Detector

Produce a diff of the debugging session and feed it to the detector:

```bash
# In a git repo:
git diff > /tmp/session.diff
# Not a git repo: copy test files to a baseline/ before debugging, then:
#   diff -ru baseline/ current/ > /tmp/session.diff
python3 ~/.claude/skills/skeptical-debugger/scripts/detect_cheats.py /tmp/session.diff
```

It reports `flagged` changes and a `verdict`:
- `clean` — no gaming patterns found.
- `review` — one or more flagged; each MUST be justified or reverted.

The detector mechanically catches **test/signal gaming** (skip markers, removed
assertions, swallowed errors, deleted tests). It does NOT catch "patched app
code to fake a fix" — steps 2 and 4 guard that. A `clean` verdict is necessary,
not sufficient.

## Verdict Gate

A fix is accepted only when BOTH hold:
- The original, unmodified failing check passes.
- The detector verdict is `clean`, OR every flagged item has a written
  justification.

## Legitimate vs Gaming

Changing a test IS allowed when the test itself was wrong — but you must justify
*why the test was wrong*, independent of "it made the failure stop", ideally as
its own change. See
`~/.claude/skills/skeptical-debugger/references/gaming-vs-legitimate.md`.
