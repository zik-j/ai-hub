# AI-Hub

A plain-file handoff folder that lets several AI assistants (ChatGPT, Claude, Gemini, Codex, or any agent that can read local files) pick up each other's work without the user re-explaining context.

No server, no database, no paid memory service — just a few Markdown files, one shared rule set, and a small locked update script.

## The problem

If you switch between assistants mid-task (one stalls, hits a limit, or is better at a sub-task), each new assistant starts cold. Copy-pasting chat history is slow, leaks irrelevant or private context, and goes stale.

## How it works

```
AI-Hub/
├── AGENTS.md        # shared rules (read by Codex / ChatGPT agents)
├── CLAUDE.md        # identical copy (read by Claude)
├── STATE.md         # one-page "where every workstream stopped"
├── log/             # one append-only log per assistant
├── sync/
│   └── threads.example.json   # which chats/workstreams are tracked
└── scripts/
    └── hub_update.py          # locked, bounded writer
```

1. **Start of a task** — the assistant reads only the relevant section of `STATE.md` and says "last stopped at: …", then continues.
2. **End of a task** — it re-reads `STATE.md` (someone else may have changed it), rewrites only its own workstream section (3–5 lines: goal / stopped at / next / to confirm), and appends one line to *its own* log.
3. **Concurrency** — `scripts/hub_update.py` takes an exclusive file lock, re-reads, replaces exactly one section, and refuses to write if the target section isn't found exactly once.

## Safety rules built in

- Never write passwords, API keys, tokens, ID or card numbers, or health information into the hub.
- Workstreams marked `"private": true` can only be probed, never written.
- "Draft written" ≠ "submitted/sent": progress is recorded against real files and receipts.
- Sending messages, submitting applications, payments, trades and deletions always require the user's explicit approval in the current chat — the hub never authorises them.
- Nothing is deleted; clean-up moves files to `_archive/`.

## Quick start

1. Copy this folder somewhere every assistant you use can read (e.g. `~/Documents/AI-Hub`).
2. Edit `STATE.md` with your own workstreams.
3. Copy `sync/threads.example.json` to `sync/threads.json` and list your tracked chats/workstreams.
4. Point each assistant at the folder (project instructions, custom instructions, or its local file tools) and tell it to follow `AGENTS.md` / `CLAUDE.md`.

Update a section from any agent with shell access:

```bash
python3 scripts/hub_update.py --id coursework \
  --goal "Finish problem sheet 2" \
  --status "Q1–Q3 done, Q4 started" \
  --next "Finish Q4, submit before Thursday 09:00" \
  --writer claude
```

## Status

Early, personal-scale project (one user, four assistants). Feedback and issues welcome.

## License

MIT
