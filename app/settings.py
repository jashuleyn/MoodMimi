from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = os.getenv("MOODMIMI_DB_PATH", str(DATA_DIR / "moodmimi.sqlite3"))
MODEL_ID = os.getenv("MOODMIMI_MODEL_ID", "boltuix/NeuroFeel")

# Set MOODMIMI_ENABLE_TRANSFORMERS=0 to force offline keyword fallback.
ENABLE_TRANSFORMERS = os.getenv("MOODMIMI_ENABLE_TRANSFORMERS", "1").strip().lower() not in {
    "0", "false", "no", "off"
}
