import json
import sqlite3
from contextlib import closing
from typing import Any, Dict, List

from .settings import DB_PATH


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    user_text TEXT NOT NULL,
    bot_reply TEXT NOT NULL,
    emotion TEXT NOT NULL,
    confidence REAL NOT NULL,
    tone TEXT NOT NULL,
    suggestion TEXT NOT NULL,
    scores_json TEXT NOT NULL,
    is_crisis INTEGER NOT NULL DEFAULT 0,
    model_used TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with closing(get_connection()) as conn:
        conn.execute(CREATE_TABLE_SQL)
        conn.commit()


def save_chat(item: Dict[str, Any]) -> int:
    with closing(get_connection()) as conn:
        cur = conn.execute(
            """
            INSERT INTO chat_messages (
                session_id, user_text, bot_reply, emotion, confidence, tone,
                suggestion, scores_json, is_crisis, model_used, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item["session_id"],
                item["user_text"],
                item["bot_reply"],
                item["emotion"],
                float(item["confidence"]),
                item["tone"],
                item["suggestion"],
                json.dumps(item["scores"], ensure_ascii=False),
                1 if item["is_crisis"] else 0,
                item["model_used"],
                item["created_at"],
            ),
        )
        conn.commit()
        return int(cur.lastrowid)


def fetch_history(limit: int = 30) -> List[Dict[str, Any]]:
    safe_limit = max(1, min(int(limit), 200))
    with closing(get_connection()) as conn:
        rows = conn.execute(
            """
            SELECT * FROM chat_messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (safe_limit,),
        ).fetchall()

    items: List[Dict[str, Any]] = []
    for row in rows:
        data = dict(row)
        data["is_crisis"] = bool(data["is_crisis"])
        try:
            data["scores"] = json.loads(data.pop("scores_json") or "[]")
        except json.JSONDecodeError:
            data["scores"] = []
        items.append(data)
    return items


def clear_history() -> None:
    with closing(get_connection()) as conn:
        conn.execute("DELETE FROM chat_messages")
        conn.commit()
