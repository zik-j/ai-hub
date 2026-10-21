# AI-Hub shared rules (ChatGPT / Claude / Gemini / Codex)

This folder is the single place where work is handed off between AI assistants. `AGENTS.md` and `CLAUDE.md` are identical — change one, change both.

## 1. At the start (do only this)
- If the task belongs to a workstream in `STATE.md`: read that section only, say in one sentence "Last stopped at: …", then continue the work.
- Read only `STATE.md`. Do **not** read `log/` unless you need to trace a detail.
- Casual Q&A or tasks unrelated to any workstream: don't read or write this folder.

## 2. At the end (after every completed task, without being asked)
1. Re-read `STATE.md` (someone else may have just changed it).
2. Edit only the relevant workstream section, 3–5 lines: Goal / Stopped at / Next / To confirm, and update "Last updated".
3. Append one line to your own log `log/<your-name>.md`: `- YYYY-MM-DD HH:MM | workstream | what was done | output file path`.
4. **Write only your own log file**; never edit another assistant's log.
5. Remove finished items that need no follow-up from `STATE.md`; the log keeps the history.

Log names: `chatgpt` / `claude` / `gemini` / `codex` (add your own).

## 3. Style
- Short sentences. Keep facts and guesses separate (mark guesses "unverified").
- Progress is based on real files and real receipts: "draft written" is not "submitted/sent".
- Keep the whole `STATE.md` within one page.

## 4. Boundaries
- Never write: passwords, API keys, tokens, ID numbers, bank/card numbers, health information.
- Sending emails/messages, submitting applications, payments, trades, deleting files: only with the user's explicit approval in the current chat.
- Never delete anything in this folder; move it to `_archive/` instead.
- This folder shares work progress only. It is not for rotating usage quotas across accounts.

## 5. Scripted updates (optional)
- Prefer `scripts/hub_update.py` when you have shell access: it locks `sync/update.lock`, re-reads, replaces exactly one section, and appends to your log.
- Workstreams marked `"private": true` in `sync/threads.json` may only be probed, never written.
- If you lack file access, say "not written back" — never claim the hub was updated when it wasn't.
