from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import clear_history, fetch_history, init_db, save_chat
from .emotion_engine import EmotionDetector, check_crisis
from .reply_engine import generate_reply
from .schemas import ChatRequest, ChatResponse
from .settings import MODEL_ID, STATIC_DIR

PH_TZ = timezone(timedelta(hours=8))

app = FastAPI(
    title="MoodMimi API",
    description="Emotion-aware chatbot prototype with text emotion detection.",
    version="1.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

detector = EmotionDetector()


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(Path(STATIC_DIR) / "index.html")


@app.get("/api/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "model_id": MODEL_ID,
        "model_loaded": detector.is_model_loaded,
        "model_used": detector.model_used,
        "model_error": detector.model_error,
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> Dict[str, Any]:
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    session_id = (request.session_id or "default").strip() or "default"
    is_crisis = check_crisis(message)

    if is_crisis:
        emotion_result = {
            "emotion": "Crisis",
            "confidence": 1.0,
            "scores": [{"label": "Crisis", "score": 1.0}],
            "model_used": "safety-layer",
        }
    else:
        emotion_result = detector.predict(message)

    reply_result = generate_reply(str(emotion_result["emotion"]), is_crisis=is_crisis)
    created_at = datetime.now(PH_TZ).isoformat(timespec="seconds")

    item = {
        "session_id": session_id,
        "user_text": message,
        "bot_reply": reply_result["reply"],
        "emotion": emotion_result["emotion"],
        "confidence": float(emotion_result["confidence"]),
        "tone": reply_result["tone"],
        "suggestion": reply_result["suggestion"],
        "scores": emotion_result["scores"],
        "is_crisis": is_crisis,
        "model_used": emotion_result["model_used"],
        "created_at": created_at,
    }
    save_chat(item)

    # Return the exact response shape expected by ChatResponse and the frontend.
    # The saved database item uses bot_reply, but the API response must use reply.
    return {
        "reply": item["bot_reply"],
        "emotion": item["emotion"],
        "confidence": item["confidence"],
        "tone": item["tone"],
        "suggestion": item["suggestion"],
        "scores": item["scores"],
        "is_crisis": item["is_crisis"],
        "model_used": item["model_used"],
        "created_at": item["created_at"],
    }


@app.get("/api/history")
def history(limit: int = Query(default=30, ge=1, le=200)) -> Dict[str, Any]:
    items = fetch_history(limit=limit)
    return {"items": items}


@app.delete("/api/history")
def delete_history() -> Dict[str, str]:
    clear_history()
    return {"status": "cleared"}
