#!/usr/bin/env python3
"""Locked, bounded updates to one STATE.md section. Never pass credentials or health details."""
import argparse
import fcntl
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
MAX_LEN = 1600


def load_manifest():
    for name in ("threads.json", "threads.example.json"):
        path = ROOT / "sync" / name
        if path.is_file():
            return json.loads(path.read_text())
    raise SystemExit("sync/threads.json not found")


def main():
    manifest = load_manifest()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--id", required=True, help="workstream id from sync/threads.json")
    p.add_argument("--probe", action="store_true", help="check read/write access only")
    p.add_argument("--goal")
    p.add_argument("--status")
    p.add_argument("--next", dest="next_step")
    p.add_argument("--writer", choices=manifest.get("writers", ["chatgpt", "claude", "gemini", "codex"]), required=True)
    a = p.parse_args()

    target = next((t for t in manifest["threads"] if t["id"] == a.id), None)
    if target is None:
        p.error("id is not listed in sync/threads.json")

    tz = ZoneInfo(manifest.get("timezone", "UTC"))
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M")
    (ROOT / "sync").mkdir(exist_ok=True)
    (ROOT / "log").mkdir(exist_ok=True)

    with (ROOT / "sync" / "update.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)

        if a.probe:
            print(json.dumps({"id": a.id, "checked_at": now,
                              "state_readable": (ROOT / "STATE.md").is_file(),
                              "rules_readable": (ROOT / "AGENTS.md").is_file()}))
            return

        if target.get("private"):
            p.error("private workstreams can only be probed, never written")
        if not all([a.goal, a.status, a.next_step]):
            p.error("--goal, --status and --next are all required")
        for v in (a.goal, a.status, a.next_step):
            if "\n" in v or len(v) > MAX_LEN:
                p.error(f"each field must be a single line of at most {MAX_LEN} characters")

        path = ROOT / "STATE.md"
        blocks = re.split(r"(?=^## )", path.read_text(), flags=re.M)
        hits = [i for i, b in enumerate(blocks) if b.splitlines()[0].strip() == f"## {a.id}"]
        if len(hits) != 1:
            raise SystemExit(f"expected exactly one '## {a.id}' section, found {len(hits)}; nothing written")

        blocks[hits[0]] = (f"## {a.id}\n- Goal: {a.goal}\n- Stopped at: {a.status}\n"
                           f"- Next / to confirm: {a.next_step}\n- Last updated: {now} {a.writer}\n\n")
        path.write_text("".join(blocks))

        with (ROOT / "log" / f"{a.writer}.md").open("a") as f:
            f.write(f"- {now} | {a.id} | {a.status} | STATE.md\n")

        print(json.dumps({"updated": True, "id": a.id, "at": now}))


if __name__ == "__main__":
    main()
