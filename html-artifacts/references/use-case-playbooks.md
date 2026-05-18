# HTML Artifact Playbooks

Detailed playbooks for the five situations where an HTML artifact beats a markdown file.

Source: "Using Claude Code: The Unreasonable Effectiveness of HTML" by Thariq Shihipar (@trq212). Examples gallery: <https://thariqs.github.io/html-effectiveness/>

The example prompts below are illustrative shapes, not magic strings — adapt them to the actual task.

---

## 1. Specs, planning & exploration

Instead of a single markdown plan, build a *web* of HTML files and walk through it:

1. **Brainstorm** → one HTML file with several distinctly different option explorations laid out in a grid for side-by-side comparison. Vary layout, tone, density. Label each with the tradeoff it makes.
2. **Expand the chosen direction** → mockups, code snippets, data-flow diagrams.
3. **Implementation plan** → one readable HTML file: mockups where there's UI (sequence / data-flow diagrams otherwise, rendered as SVG), the key code snippets the reviewer will want, organized so it's easy to digest.
4. **Implement in a fresh session**, passing in all the HTML files for full context. Have the verification agent read them too — it gets much broader context on what's needed.

Example prompts:
- "I'm not sure what direction to take the onboarding screen. Generate 6 distinctly different approaches — vary layout, tone, and density — and lay them out as a single HTML file in a grid so I can compare them side by side. Label each with the tradeoff it's making."
- "Create a thorough implementation plan in an HTML file, be sure to make some mockups, show data flow and add important code snippets I might want to review. Make it easy to read and digest."

Good for: exploring alternative ways to implement something in code; exploring multiple visual designs.

---

## 2. Code review & understanding

Code is hard to read in a markdown file. In HTML you can render diffs, inline annotations, flowcharts, module maps. Use it to understand code the agent wrote, to get a code review, or to explain a PR to a reviewer — it often works better than the default GitHub diff view. Consider attaching an HTML explainer to every PR.

Put in it: the actual diff rendered with inline margin annotations; findings color-coded by severity; flowcharts of the tricky logic; a module/dependency map; whatever conveys the concept best.

Example prompt:
- "Help me review this PR by creating an HTML artifact that describes it. I'm not very familiar with the streaming/backpressure logic so focus on that. Render the actual diff with inline margin annotations, color-code findings by severity and whatever else might be needed to convey the concept well."

Good for: creating a PR writeup; reviewing a PR; understanding a topic in code.

---

## 3. Design & prototypes

HTML is incredibly expressive for design even when the end surface is not HTML — sketch the design in HTML, then port to React, Swift, etc. You can also prototype interactions (animations, actions) and add sliders/knobs to tune in exactly what you want.

Put in it: the design rendered in HTML/CSS; controls (sliders, dropdowns, toggles) for the parameters being tuned; a "copy parameters" button that emits the values that worked.

Example prompt:
- "I want to prototype a new checkout button — when clicked it does a play animation and then turns purple quickly. Create an HTML file with several sliders and options for me to try different options on this animation; give me a copy button to copy the parameters that worked well."

Good for: design-system artifacts; adjusting components; visualizing component libraries; prototyping joyful animations.

---

## 4. Reports, research & learning

Claude Code is good at synthesizing across sources — codebase, git history, Slack/Linear MCPs, the web — and turning it into something readable for yourself, your team, or leadership. Deliver it as a long HTML document, an interactive explainer, or a slideshow/deck. Use SVG for diagrams.

Put in it: a clear narrative; SVG diagrams/flowcharts of the mechanism; the 3–4 key code snippets, annotated; a "gotchas" section at the bottom. Optimize it for someone reading it once.

Example prompt:
- "I don't understand how our rate limiter actually works. Read the relevant code and produce a single HTML explainer page: a diagram of the token-bucket flow, the 3–4 key code snippets annotated, and a 'gotchas' section at the bottom. Optimize it for someone reading it once."

Good for: summarizing how a feature works; explaining a concept; weekly status reports to your boss; incident reports to leadership; SVG illustrations, flowcharts, and technical diagrams.

---

## 5. Custom editing interfaces

When it's hard to describe what you want in a text box, build a throwaway editor — not a product, not a reusable tool, just a single HTML file purpose-built for this one piece of data. **The trick is always to end with an export:** a "copy as JSON" / "copy as prompt" / "copy diff" button that turns whatever you did in the UI back into something you can paste into Claude Code.

Example prompts:
- "I need to reprioritize these 30 Linear tickets. Make me an HTML file with each ticket as a draggable card across Now / Next / Later / Cut columns. Pre-sort them by your best guess. Add a 'copy as markdown' button that exports the final ordering with a one-line rationale per bucket."
- "Here's our feature flag config. Build a form-based editor for it — group flags by area, show dependencies between them, warn me if I enable a flag whose prerequisite is off. Add a 'copy diff' button that gives me just the changed keys."
- "I'm tuning this system prompt. Make a side-by-side editor: editable prompt on the left with the variable slots highlighted, three sample inputs on the right that re-render the filled template live. Add a character/token counter and a copy button."

Good for: reordering / triaging / bucketing anything (tickets, test cases, feedback); editing structured config with constraints (feature flags, env vars, JSON/YAML); tuning prompts, templates, or copy with live preview; curating datasets (approve/reject rows, tag examples, export the selection); annotating a document, transcript, or diff and exporting the annotations; picking values that are painful to express in text — colors, easing curves, crop regions, cron schedules, regexes.

---

## FAQ (from the article)

- **Isn't it less token-efficient?** Markdown uses fewer tokens, but HTML's expressiveness — and the much higher chance the human actually reads it — makes the net outcome better. With a ~1M context window the extra tokens aren't noticeable.
- **How do I view the HTML file?** Open it in a browser locally (you can ask Claude to open it), or upload to S3 for a shareable link.
- **Doesn't it take longer to generate?** Yes — roughly 2–4× longer than markdown. Usually worth it for artifacts that get read and shared.
- **What about version control?** The biggest downside: HTML diffs are noisy and hard to review. For docs that must be reviewed via diff, stay in markdown.
- **How do I keep it from being ugly / match my taste?** Use a frontend-design / design-taste skill for general quality. For house style, point Claude at the codebase to generate one design-system HTML file, then reference that file from other artifacts.
- **When do I still use markdown?** Short outputs, throwaway intermediate notes, and anything reviewed via diff. (The article author reports he's stopped using markdown for almost everything — but he's on the maximalist end; this skill keeps it a judgment call.)
