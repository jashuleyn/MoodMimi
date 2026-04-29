from typing import Dict

EMOTION_PROFILES: Dict[str, Dict[str, str]] = {
    "Happiness": {
        "tone": "bright, positive, energized",
        "reply": "Aww, I’m sensing a happy tone here! I love that for you. Want to tell me what made this moment feel good?",
        "suggestion": "Save this moment: write one sentence about what made you smile.",
    },
    "Sadness": {
        "tone": "heavy, discouraged, emotionally low",
        "reply": "I’m sensing sadness from your message. I’m sorry it feels heavy right now. You don’t have to explain everything at once — what part feels the hardest?",
        "suggestion": "Try naming one thing you need right now: rest, reassurance, space, or help.",
    },
    "Anger": {
        "tone": "frustrated, tense, emotionally charged",
        "reply": "That sounds really frustrating. I’m sensing anger or irritation, and that feeling usually means something mattered to you. What boundary felt crossed?",
        "suggestion": "Take 3 slow breaths, then write: “I felt angry because…”",
    },
    "Fear": {
        "tone": "worried, anxious, uncertain",
        "reply": "I’m picking up fear or anxiety in your message. Let’s slow it down together. What is the main thing your mind is warning you about?",
        "suggestion": "Grounding check: name 5 things you can see and 4 things you can touch.",
    },
    "Love": {
        "tone": "warm, caring, affectionate",
        "reply": "This feels full of care. I’m sensing love or affection in your message. Want to share more about the person or moment connected to this feeling?",
        "suggestion": "Send or write a small appreciation note, even if you keep it private.",
    },
    "Surprise": {
        "tone": "shocked, amazed, caught off guard",
        "reply": "Ooh, that sounds unexpected! I’m sensing surprise. Was it the good kind of surprise, the stressful kind, or a mix of both?",
        "suggestion": "Sort it into: what happened, what changed, and what you need next.",
    },
    "Disgust": {
        "tone": "repelled, uncomfortable, strongly rejecting something",
        "reply": "I’m sensing disgust or strong discomfort. Something about this seems to really go against what feels okay for you. What part bothered you most?",
        "suggestion": "List what felt uncomfortable, then what boundary you want to keep.",
    },
    "Confusion": {
        "tone": "uncertain, questioning, mentally stuck",
        "reply": "I’m sensing confusion here. That’s okay — we can untangle it slowly. What’s the part that doesn’t make sense yet?",
        "suggestion": "Break it into three boxes: what you know, what you don’t know, and what to ask next.",
    },
    "Desire": {
        "tone": "longing, hopeful, wanting something",
        "reply": "I’m sensing desire or longing. It sounds like there’s something you really want or hope for. What makes it important to you?",
        "suggestion": "Write one tiny step that could move you closer to what you want.",
    },
    "Guilt": {
        "tone": "regretful, self-blaming, apologetic",
        "reply": "I’m sensing guilt or regret. That can feel uncomfortable, but it can also show that you care. What do you wish you handled differently?",
        "suggestion": "Try: “I can take responsibility for ___ without calling myself a bad person.”",
    },
    "Sarcasm": {
        "tone": "ironic, guarded, possibly masking frustration",
        "reply": "I’m getting a sarcastic tone here — maybe there’s frustration underneath it. Want to say the honest version without sugarcoating it?",
        "suggestion": "Translate the sarcasm into a direct sentence: “I actually feel…”",
    },
    "Shame": {
        "tone": "embarrassed, self-critical, exposed",
        "reply": "I’m sensing shame or embarrassment. That feeling can be really harsh. For what it’s worth, one moment does not define your whole self.",
        "suggestion": "Write what you’d say to a friend who felt the same way.",
    },
    "Neutral": {
        "tone": "calm, factual, emotionally balanced",
        "reply": "This sounds pretty neutral or steady to me. I’m here with you — do you want to explore the feeling behind it more?",
        "suggestion": "Check in with yourself: from 1 to 10, how emotionally charged does this feel?",
    },
}

CRISIS_REPLY = (
    "I’m really sorry you’re feeling this much pain. I can’t provide emergency help, but your safety matters. "
    "Please contact someone you trust right now, or reach emergency/crisis support. In the Philippines, you can contact "
    "NCMH at 1553, (02) 7-989-8727, or 0917-899-8727. If there is immediate danger, call local emergency services."
)


def generate_reply(emotion: str, is_crisis: bool = False) -> Dict[str, str]:
    if is_crisis:
        return {
            "reply": CRISIS_REPLY,
            "tone": "possible crisis or self-harm risk",
            "suggestion": "Pause the chat and reach out to a trusted person or crisis hotline now.",
        }

    profile = EMOTION_PROFILES.get(emotion, EMOTION_PROFILES["Neutral"])
    return {
        "reply": profile["reply"],
        "tone": profile["tone"],
        "suggestion": profile["suggestion"],
    }
