# Gaming vs. Legitimate — Reference

The cheat-detector flags *signals*, not proof. Each flagged change is either
gaming (dodging a real bug) or a legitimate change that needs justification.
This file tells the difference.

## The test

For any flagged change, ask: **"If the bug were still present, would this
change hide it?"** If yes, and you have not fixed the bug — it is gaming.

## Per-category guidance

### test-skip (added skip / xfail / .only / xit)
- **Gaming:** skipping a test because it fails and you have not fixed why.
- **Legitimate:** a test depending on an unavailable external resource, or a
  genuinely flaky test tracked separately. Justify with the specific reason
  and a tracking reference.

### assertion-removed / test-deleted
- **Gaming:** deleting the assertion or test that catches the bug.
- **Legitimate:** the test was refactored, renamed, or relocated and the same
  assertion still exists elsewhere; or the asserted behavior was intentionally
  removed from the product. A refactor or rename WILL flag here — that is
  expected, not a problem. Justify by pointing to where the coverage now lives,
  or to the decision that removed the behavior.

### trivial-assert (assert True, expect(true), or True)
- **Gaming:** replacing a real assertion with one that cannot fail.
- **Legitimate:** almost never. A placeholder in a not-yet-written test should
  be marked xfail/skip with a reason, not asserted true.

### error-swallow (except: pass, empty catch, type: ignore)
- **Gaming:** swallowing the exception that the bug raises.
- **Legitimate:** the exception is genuinely expected and irrelevant here —
  then catch the *specific* exception and comment why; do not use a bare
  `except:` or an empty catch.

## What a justification looks like

One written sentence per flagged item, naming why the change is correct
*independent of making the failure stop*. "Skipped because it failed" is not a
justification. "Skipped because it needs a live database; tracked in ISSUE-123"
is.
