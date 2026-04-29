# MoodMimi: Emotion-Aware Chatbot Prototype

MoodMimi is a SimSimi-inspired chatbot prototype that detects the emotional tone of a user's text message, shows the detected emotion and confidence score, changes the mascot reaction, saves chat history in SQLite, and replies with supportive non-diagnostic responses.

> Important: This is a school/prototype app. It is **not** a therapist, not a medical device, and does not diagnose mental health conditions.

## Features

- Cute mascot-based chatbot UI
- Text emotion detection through Hugging Face `boltuix/NeuroFeel`
- Keyword-based fallback emotion detector if the model cannot load
- 13-emotion support: happiness, disgust, sadness, love, surprise, fear, neutral, confusion, desire, anger, guilt, sarcasm, shame
- Emotion result card with confidence score and top predictions
- SQLite chat/emotion history
- Mood count chart
- Crisis keyword safety layer with Philippine NCMH contact info
- Full-stack structure: HTML, CSS, JavaScript, Python FastAPI, SQLite

## Tech Stack

```txt
Frontend: HTML + CSS + Vanilla JavaScript
Backend: Python + FastAPI
Model: Hugging Face Transformers + boltuix/NeuroFeel
Database: SQLite
```

## Project Structure

```txt
moodmimi_app/
├─ app/
│  ├─ main.py
│  ├─ settings.py
│  ├─ schemas.py
│  ├─ database.py
│  ├─ emotion_engine.py
│  ├─ reply_engine.py
│  └─ static/
│     ├─ index.html
│     ├─ styles.css
│     └─ script.js
├─ data/
│  └─ moodmimi.sqlite3   # auto-created after first run
├─ requirements.txt
├─ run_windows.bat
├─ run_mac_linux.sh
└─ README.md
```

## Setup

Recommended Python version: **Python 3.10 to 3.12**.

### Windows PowerShell

```powershell
cd moodmimi_app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```txt
http://127.0.0.1:8000
```

### macOS / Linux

```bash
cd moodmimi_app
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```txt
http://127.0.0.1:8000
```

## Faster Demo Mode / Offline Fallback

The first normal run may download the Hugging Face model. If you have weak internet or want to demo immediately, disable the transformer model and use the built-in fallback detector.

### Windows PowerShell

```powershell
$env:MOODMIMI_ENABLE_TRANSFORMERS="0"
uvicorn app.main:app --reload
```

### macOS / Linux

```bash
MOODMIMI_ENABLE_TRANSFORMERS=0 uvicorn app.main:app --reload
```

## API Endpoints

### `POST /api/chat`

Request:

```json
{
  "message": "I feel so tired and alone today.",
  "session_id": "demo-session"
}
```

Response:

```json
{
  "reply": "I’m really sorry it feels this heavy right now...",
  "emotion": "Sadness",
  "confidence": 0.87,
  "tone": "heavy, discouraged, emotionally low",
  "suggestion": "Write one sentence about what you wish someone understood.",
  "scores": [
    {"label": "Sadness", "score": 0.87},
    {"label": "Fear", "score": 0.07}
  ],
  "is_crisis": false,
  "model_used": "boltuix/NeuroFeel",
  "created_at": "2026-04-29T12:00:00+08:00"
}
```

### `GET /api/history`

Returns recent chat/emotion history.

### `DELETE /api/history`

Clears saved history.

### `GET /api/health`

Checks whether the app and model are loaded.

## Notes for Defense / Presentation

- The prototype uses emotion classification, not clinical diagnosis.
- The model output should be described as an estimated emotional tone.
- The crisis layer is rule-based and designed to interrupt normal chatbot behavior when high-risk phrases appear.
- For a stronger research version, you can fine-tune the model on more local/contextual English, Taglish, and Filipino emotional expression data.

## References

- NeuroFeel model: https://huggingface.co/boltuix/NeuroFeel
- boltuix emotions dataset: https://huggingface.co/datasets/boltuix/emotions-dataset
- FastAPI static files: https://fastapi.tiangolo.com/tutorial/static-files/
- MentalHealthPH emergency help: https://mentalhealthph.org/help/
