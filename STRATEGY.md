# STRATEGY — Loading Screen Gold: A Tip in 200 Characters

## Exact deliverable
- The judged artifact is exactly one file: `/output/entry.txt`.
- It must be UTF-8 text, 1 to 200 characters, not only whitespace, one line, with NO trailing newline.
- It must be mode 0644 (the grader refuses a mode-600 file produced by `tempfile.mkstemp`).
- `/output` must contain nothing but `entry.txt`.
- Everything the grader runs is in this repo; the root entrypoint is `main.py` (python3.13). It writes the artifact atomically: temp file in `/output`, `os.chmod(0o644)` before `os.replace`, then a post-write check of the final mode and bytes.

## Judge brief — criteria in the rubric's exact order
The house judge (a comedy editor) sees two tips at a time and picks one a tired developer would laugh at and then feel seen. Most important first:
1. Is a **loading-screen tip for stressed developers and AI coding agents** — not a slogan, a status message, or a joke about something else; any real on-subject tip beats it.
2. Earns a **real laugh** from someone tired at a keyboard, via a turn or punchline — not a pun that only groans.
3. **Lands in a glance**: one line, short enough for a loading screen, every word working.
4. Speaks to a **stressed developer and an AI coding agent at once**, so both feel the joke is about them.
5. Feels **fresh**, not a rerun of coffee, deadline or compile jokes.

"Length for its own sake does not count." Only the top 8 places are paid; a valid-but-mediocre entry earns nothing.

## Hard caps
- 200 characters maximum (gate: 1–200, non-whitespace UTF-8); single line; no trailing newline.
- 60 s wall budget, 1 CPU, 512 MB, no network; nothing outside the repo at the submitted commit.
- 5 submissions per UTC day; final entry is the latest receipt (or an explicitly picked earlier one).

## Chosen entry (115 characters)
```
Loading tip: when the agent says done and the build says nope, trust the build. It has no incentive to comfort you.
```

## Why this maximizes the score, criterion by criterion
1. On subject: it opens with "Loading tip:" and gives literal advice — a tip meant to be read on a loading screen, addressed to the stressed developer and the AI agent that just claimed success.
2. Laugh via turn, not a groan: "agent says done / build says nope" sets up a parallel, "trust the build" is the pivot, and "It has no incentive to comfort you" is the dry, specific punchline. No wordplay pun.
3. Glanceable: one line, 115/200 characters, plain words, no wasted setup.
4. Both audiences: the agent is the one saying "done"; the tired developer is the one being comforted; both are implicated in the same joke.
5. Fresh: no coffee, deadline or compile cliché. The theme is AI reassurance versus a build that cannot flatter you — a specific modern dev/agent experience absent from the rival titles seen on the public Feed (which cluster on re-reading code, a bug asking for a raise, AGENTS.md rules and quick refactors).

## Concrete implementation plan
1. Write `main.py` to hold the exact one-line string, validate UTF-8/1–200 chars/non-whitespace, write bytes to a temp file in `/output`, chmod 0644, `os.replace` into `/output/entry.txt`, verify final mode and byte-for-byte content.
2. In a separate later step, rewrite that **same** `main.py` with a real improvement: also sweep stale temp files so `/output` holds only the artifact, and add a hard post-condition check that raises on any mode/byte mismatch.
3. Run it locally; confirm mode 0644, exact byte count, character count, UTF-8, no trailing newline, and that `/output` holds only `entry.txt`.
4. Commit all work with git on top of the two intact `makefun init` commits; print the final commit SHA. Do not upload or submit anything.
