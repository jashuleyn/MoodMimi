import logging
import math
import re
from typing import Dict, List

from .settings import ENABLE_TRANSFORMERS, MODEL_ID

logger = logging.getLogger(__name__)

DATASET_LABELS = [
    "happiness",
    "disgust",
    "sadness",
    "love",
    "surprise",
    "fear",
    "neutral",
    "confusion",
    "desire",
    "anger",
    "guilt",
    "sarcasm",
    "shame",
]

LABEL_ALIASES = {
    "joy": "happiness",
    "happy": "happiness",
    "sad": "sadness",
    "angry": "anger",
    "scared": "fear",
    "afraid": "fear",
    "surprised": "surprise",
    "loving": "love",
    "neutrality": "neutral",
}

CRISIS_PATTERNS = [
    r"\bkill myself\b",
    r"\bend my life\b",
    r"\bi want to die\b",
    r"\bi wanna die\b",
    r"\bsuicide\b",
    r"\bsuicidal\b",
    r"\bself[-\s]?harm\b",
    r"\bhurt myself\b",
    r"\bi don't want to live\b",
    r"\bi do not want to live\b",
    r"\bno reason to live\b",
]

KEYWORD_LEXICON = {
    "happiness": [
        "happy", "joy", "excited", "proud", "grateful", "glad", "good", "great", "yay",
        "cheerful", "blessed", "relieved", "awesome", "fun", "smile", "laugh",
    ],
    "sadness": [
        "sad", "lonely", "alone", "cry", "crying", "tired", "empty", "hurt", "broken",
        "miss", "grief", "down", "depressed", "heavy", "disappointed", "hopeless",
    ],
    "anger": [
        "angry", "mad", "furious", "annoyed", "irritated", "hate", "unfair", "ridiculous",
        "frustrated", "rage", "pissed", "upset", "sick of", "fed up",
    ],
    "fear": [
        "afraid", "scared", "worried", "anxious", "panic", "terrified", "nervous", "unsafe",
        "overthinking", "stress", "stressed", "fear", "dread", "what if",
    ],
    "love": [
        "love", "loved", "care", "caring", "crush", "affection", "adore", "miss you", "heart",
        "comfort", "hug", "sweet", "cherish",
    ],
    "surprise": [
        "wow", "shocked", "surprised", "unexpected", "suddenly", "omg", "no way", "can't believe",
        "unbelievable", "amazed",
    ],
    "disgust": [
        "gross", "disgusting", "ew", "nasty", "sickening", "creepy", "repulsed", "yuck",
    ],
    "confusion": [
        "confused", "lost", "unclear", "idk", "i don't know", "what", "why", "how", "huh",
        "don't get", "doesn't make sense", "mixed up",
    ],
    "desire": [
        "want", "wish", "hope", "need", "crave", "dream", "goal", "longing", "manifest",
    ],
    "guilt": [
        "guilty", "fault", "my fault", "sorry", "regret", "ashamed of what i did", "blame myself",
        "should have", "should've",
    ],
    "shame": [
        "ashamed", "embarrassed", "humiliated", "worthless", "not enough", "failure", "fail",
        "disappointing", "disappointed in myself",
    ],
    "sarcasm": [
        "yeah right", "sure", "as if", "totally", "obviously", "wow thanks", "great job", "nice one",
    ],
    "neutral": [
        "okay", "fine", "normal", "nothing", "today", "message", "update", "schedule",
    ],
}


def title_label(label: str) -> str:
    if not label:
        return "Neutral"
    return label.strip().replace("_", " ").replace("-", " ").title()


def check_crisis(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in CRISIS_PATTERNS)


class EmotionDetector:
    def __init__(self) -> None:
        self.model_id = MODEL_ID
        self.classifier = None
        self.model_error = None
        self.model_used = "keyword-fallback"
        self.load_model()

    @property
    def is_model_loaded(self) -> bool:
        return self.classifier is not None

    def load_model(self) -> None:
        if not ENABLE_TRANSFORMERS:
            self.model_error = "Transformer loading disabled by MOODMIMI_ENABLE_TRANSFORMERS=0."
            logger.info(self.model_error)
            return

        try:
            from transformers import pipeline

            self.classifier = pipeline(
                "text-classification",
                model=self.model_id,
                tokenizer=self.model_id,
                top_k=None,
            )
            self.model_used = self.model_id
            logger.info("Loaded emotion model: %s", self.model_id)
        except Exception as exc:  # pragma: no cover - depends on local environment/network
            self.classifier = None
            self.model_error = str(exc)
            self.model_used = "keyword-fallback"
            logger.warning("Could not load transformer model. Using fallback. Error: %s", exc)

    def predict(self, text: str) -> Dict[str, object]:
        cleaned = text.strip()
        if not cleaned:
            return self._fallback_predict("neutral")

        if self.classifier is not None:
            try:
                raw_output = self.classifier(cleaned, truncation=True, max_length=64)
                scores = self._parse_pipeline_output(raw_output)
                if scores:
                    best = scores[0]
                    return {
                        "emotion": best["label"],
                        "confidence": round(float(best["score"]), 4),
                        "scores": scores[:5],
                        "model_used": self.model_used,
                    }
            except Exception as exc:  # pragma: no cover - depends on model runtime
                self.model_error = str(exc)
                logger.warning("Transformer prediction failed. Using fallback. Error: %s", exc)

        return self._fallback_predict(cleaned)

    def _parse_pipeline_output(self, raw_output) -> List[Dict[str, float]]:
        # Transformers can return either: [{label, score}, ...]
        # or [[{label, score}, ...]] depending on version/top_k.
        if isinstance(raw_output, list) and raw_output and isinstance(raw_output[0], list):
            rows = raw_output[0]
        elif isinstance(raw_output, list):
            rows = raw_output
        else:
            rows = []

        parsed: List[Dict[str, float]] = []
        for item in rows:
            if not isinstance(item, dict):
                continue
            label = self._normalize_label(str(item.get("label", "neutral")))
            score = float(item.get("score", 0.0))
            if math.isnan(score):
                score = 0.0
            parsed.append({"label": title_label(label), "score": round(score, 4)})

        parsed.sort(key=lambda x: x["score"], reverse=True)
        return parsed

    def _normalize_label(self, label: str) -> str:
        raw = label.strip().lower().replace("-", "_")

        # Common Hugging Face sequence classification output style: LABEL_0, LABEL_1, etc.
        match = re.fullmatch(r"label[_ ]?(\d+)", raw)
        if match:
            idx = int(match.group(1))
            if 0 <= idx < len(DATASET_LABELS):
                return DATASET_LABELS[idx]

        raw = raw.replace("_", " ").strip()
        raw = LABEL_ALIASES.get(raw, raw)
        if raw in DATASET_LABELS:
            return raw

        # Last resort: use neutral instead of exposing unknown model internals.
        return "neutral"

    def _fallback_predict(self, text: str) -> Dict[str, object]:
        lowered = f" {text.lower()} "
        counts: Dict[str, int] = {label: 0 for label in DATASET_LABELS}

        for emotion, keywords in KEYWORD_LEXICON.items():
            for keyword in keywords:
                pattern = r"(?<![a-zA-Z])" + re.escape(keyword.lower()) + r"(?![a-zA-Z])"
                if re.search(pattern, lowered):
                    counts[emotion] += 1

        best_label = max(counts, key=counts.get)
        best_count = counts[best_label]

        if best_count == 0:
            best_label = "neutral"
            scores = [{"label": "Neutral", "score": 0.62}]
        else:
            total = sum(counts.values())
            scores = []
            for label, count in counts.items():
                if count > 0:
                    score = 0.35 + (count / max(total, 1)) * 0.55
                    scores.append({"label": title_label(label), "score": round(min(score, 0.95), 4)})
            scores.sort(key=lambda x: x["score"], reverse=True)

            if not any(item["label"] == "Neutral" for item in scores):
                scores.append({"label": "Neutral", "score": 0.08})

        best_score = float(scores[0]["score"])
        return {
            "emotion": title_label(best_label),
            "confidence": round(best_score, 4),
            "scores": scores[:5],
            "model_used": "keyword-fallback",
        }
