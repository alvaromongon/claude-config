"""Builders for fake Claude Code transcripts, shaped like the JSONL files in ~/.claude/projects."""
import json
from pathlib import Path

_counter = 0


def _next_id(prefix: str) -> str:
    global _counter
    _counter += 1
    return f"{prefix}{_counter}"


def usage(input_tokens=0, cache_write_5m=0, cache_write_1h=0, cache_read=0, output_tokens=0) -> dict:
    return {
        "input_tokens": input_tokens,
        "cache_creation_input_tokens": cache_write_5m + cache_write_1h,
        "cache_read_input_tokens": cache_read,
        "output_tokens": output_tokens,
        "cache_creation": {"ephemeral_5m_input_tokens": cache_write_5m,
                           "ephemeral_1h_input_tokens": cache_write_1h},
    }


def assistant(ts, model="claude-opus-5-5", msg_id=None, content=None, **usage_kwargs) -> dict:
    return {"type": "assistant", "timestamp": ts,
            "message": {"id": msg_id or _next_id("msg_"), "model": model, "role": "assistant",
                        "content": content or [], "usage": usage(**usage_kwargs)}}


def human(ts, text) -> dict:
    return {"type": "user", "timestamp": ts, "origin": {"kind": "human"},
            "message": {"role": "user", "content": text}}


def notification(ts, text) -> dict:
    return {"type": "user", "timestamp": ts, "origin": {"kind": "task-notification"},
            "message": {"role": "user", "content": text}}


def tool_use(name, tool_id=None, **tool_input) -> dict:
    return {"type": "tool_use", "id": tool_id or _next_id("toolu_"), "name": name, "input": tool_input}


def tool_result(ts, tool_id, text, is_error=False) -> dict:
    return {"type": "user", "timestamp": ts,
            "message": {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tool_id, "content": text, "is_error": is_error}]}}


def limit_hit(ts) -> dict:
    return {"type": "assistant", "timestamp": ts,
            "message": {"id": _next_id("synthetic_"), "model": "<synthetic>", "role": "assistant",
                        "content": [{"type": "text", "text": "You've hit your session limit · resets 2:40am"}],
                        "usage": usage()}}


def write_jsonl(path: Path, events: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(e) + "\n" for e in events), encoding="utf-8")
    return path


def write_session(project: Path, session_id: str, events: list[dict], subagents=()) -> Path:
    """Write a main transcript plus subagents, each given as (agent_id, meta, events)."""
    main = write_jsonl(project / f"{session_id}.jsonl", events)
    for agent_id, meta, agent_events in subagents:
        folder = project / session_id / "subagents"
        write_jsonl(folder / f"agent-{agent_id}.jsonl", agent_events)
        (folder / f"agent-{agent_id}.meta.json").write_text(json.dumps(meta), encoding="utf-8")
    return main
