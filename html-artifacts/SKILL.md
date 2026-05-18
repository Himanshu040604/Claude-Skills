---
name: html-artifacts
description: Use when an agent's output would be a long markdown file that gets skimmed — a spec, implementation plan, design exploration, code or PR review, research report, status update, or slide deck — or a one-off editing/triage/tuning interface, i.e. when tables, diffs, diagrams, color, or interactive controls communicate better than plain text. Not for short answers, trivial edits, or docs that live in version control and are reviewed via diff.
---

# HTML Artifacts

## Overview

Markdown is the default agent output format, but it caps out fast: a 100+ line markdown spec doesn't get read, ASCII diagrams are weak, "color" becomes unicode hacks, and you can't share or interact with it. **For specs, plans, reviews, reports, and throwaway tools, an HTML file is usually the better artifact** — denser, more readable, shareable as a link, optionally interactive.

This skill is about *recognizing when an HTML artifact beats a markdown file* and *what to put in it* — it is **not** "always emit HTML" (see the markdown side of the table below).

Distilled from "Using Claude Code: The Unreasonable Effectiveness of HTML" by Thariq Shihipar. Expanded playbooks and example prompts: `references/use-case-playbooks.md`.

## HTML vs markdown — pick HTML when ANY of these holds

- The output is **longer than ~one screen** (specs, plans, reports) — HTML gets tabs, sections, sticky nav.
- It needs **tables, diffs, SVG diagrams, color, math, syntax-highlighted code, or images** — markdown degrades to ASCII art.
- You'll **share it** with someone who won't open a `.md` — HTML opens in any browser; upload to S3 for a link.
- You want to **interact**: sliders to tune a design, draggable cards to triage, a live-preview editor.
- It's **synthesis across sources** (codebase + git history + Slack + web) that benefits from rich layout.

Stay with **markdown / plain text** when the output is short (a few paragraphs, a small list, a direct answer), lives in version control and is reviewed via diff (HTML diffs are noisy), or is a throwaway intermediate note. HTML also takes ~2–4× longer to generate — spend that on artifacts people read and share, not on every message.

## The five playbooks

| Situation | Put in the HTML | And tell the user how to… |
|---|---|---|
| **Specs / planning / exploration** | Side-by-side option grid (label each with its tradeoff); mockups where there's UI (sequence / data-flow diagrams otherwise, as SVG); key code snippets; tabbed sections. Build a *web* of files: explore → expand one → implementation plan. | open it in a browser; pass the files into a fresh session to implement |
| **Code review / PR writeup** | Rendered diff with inline margin annotations; findings color-coded by severity; flowcharts of changed logic; module map. Often beats GitHub's diff view. | attach it to the PR |
| **Design / prototypes** | The design in HTML/CSS; sliders & knobs for animation / spacing / color params; a "copy parameters" button. Expressive even when the target is React/Swift. | copy the params that worked back into a prompt |
| **Reports / research / learning** | Long-form explainer, interactive explainer, or slide deck; SVG diagrams; annotated code snippets; a "gotchas" section. Optimize for *read once*. | read it / send it up the chain |
| **Custom editing interfaces** | A throwaway, purpose-built UI: draggable cards (triage), constrained config form, live-preview prompt editor, dataset approve/reject, annotation tool, painful-value pickers (color / easing / cron / regex). | **always end with an export** — a "copy as JSON / prompt / diff" button that turns the UI state back into something pasteable into Claude Code |

## Make it good

- **Gather the inputs first.** A PR writeup needs `git diff` / `gh pr diff`; an explainer needs you to read the relevant code. Get the material into context before you start building the artifact.
- **Start from `assets/starter.html`** — a self-contained, no-CDN, responsive skeleton (tabs, code block, SVG, card grid, export stub). Adapt it; trim down to what you need rather than piling on (it's near 100 lines by design).
- **One self-contained `.html` file** — inline the CSS and JS, no build step, no external CDN — so it opens locally and uploads as a single file.
- **For interactive artifacts the export button is non-negotiable** — a "copy as JSON / prompt / diff" that turns the UI state back into something pasteable into Claude Code. An editor with no way out is a dead end.
- **Keep the CSS lean.** Lift from the user's design-system file or a frontend-design / design-taste skill instead of hand-rolling 200 lines.
- **To match house style,** generate one design-system HTML file from the user's codebase once, then reference it from later artifacts. (Skip this for a single throwaway request — `starter.html` is enough.)
- **Tell the user how to view it:** offer to open it in their browser, or to put it somewhere linkable (e.g. S3) for sharing.
- **It's a judgment call, not a rule.** Short answers, throwaway notes, and diff-reviewed docs stay markdown — the failure modes are just the negatives of the points above.
