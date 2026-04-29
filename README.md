<div align="center">

# 🌼 MoodMimi

### Emotion-Aware Chatbot — Affective Computing Prototype

<img src="https://img.shields.io/badge/Python-FastAPI-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
<img src="https://img.shields.io/badge/NLP-Emotion%20Detection-ff69b4?style=for-the-badge" />
<img src="https://img.shields.io/badge/Prototype-Affective%20Computing-9b5de5?style=for-the-badge" />

</div>

---

> 🌈 This project was made as a school requirement for the subject **Current Trends and Topics in Computing**.

---

## 📖 About

**MoodMimi** is a web-based emotion-aware chatbot prototype that detects the emotional tone behind a user's message and responds with supportive, reflective prompts.

The project focuses on **Affective Computing**, a field of computing that explores how systems can recognize, interpret, and respond to human emotions. Through text-based emotion detection, MoodMimi demonstrates how artificial intelligence can be used to create more emotionally aware and human-centered digital interactions.

MoodMimi is designed with a cute mascot-inspired interface, similar to playful chatbot companions, but with the added ability to identify emotions such as happiness, sadness, anger, fear, confusion, love, surprise, and more.

> ⚠️ **Disclaimer:** MoodMimi is not a mental health diagnosis tool. It is only a prototype for educational and demonstration purposes.

---

## ✨ Features

- **Landing Page** — Welcomes users before entering the chatbot interface  
- **Chatbot Interface** — Allows users to send messages and receive replies from MoodMimi  
- **Emotion Detection** — Detects the emotional tone of a user’s message  
- **Confidence Score** — Displays how confident the system is with the detected emotion  
- **Mascot Mood Reaction** — MoodMimi changes expression based on the detected emotion  
- **Mini Reflection Activity** — Suggests short reflective prompts depending on the emotion  
- **Mood History** — Tracks recently detected emotions  
- **Crisis Safety Layer** — Shows a supportive safety message for crisis-related inputs  
- **Fallback Mode** — Uses keyword-based detection if the AI model cannot load  

---

## 🧠 What is Affective Computing?

**Affective Computing** is a branch of computing that deals with systems capable of recognizing, interpreting, processing, and responding to human emotions.

In MoodMimi, affective computing is applied through:

- text-based emotion recognition,
- natural language processing,
- emotional tone analysis,
- human-computer interaction,
- and supportive chatbot responses.

This makes MoodMimi more than just a simple chatbot. It becomes a prototype that demonstrates how machines can respond in a more emotionally aware and user-centered way.

---

## 🛠️ Tech Stack

| Category | Tools / Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI, Uvicorn |
| AI / NLP | Hugging Face Transformers, NeuroFeel Model |
| Database | SQLite |
| Prototype Focus | Affective Computing, Emotion Detection, Human-Centered AI |

---

## 📂 Project Structure

```text
MoodMimi/
│
├── app/
│   ├── static/
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── script.js
│   │
│   ├── database.py
│   ├── emotion_engine.py
│   ├── main.py
│   ├── reply_engine.py
│   ├── schemas.py
│   └── settings.py
│
├── requirements.txt
├── run_windows.bat
├── run_mac_linux.sh
└── README.md
```

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/jashuleyn/MoodMimi.git
cd MoodMimi
```

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

Then open your browser and go to:

```text
http://127.0.0.1:8000
```

---

## ⚙️ Optional: Run in Fallback Mode

If the Hugging Face model takes too long to download or fails to load, you can run MoodMimi using its keyword-based fallback detector.

For Windows PowerShell:

```powershell
$env:MOODMIMI_ENABLE_TRANSFORMERS="0"
uvicorn app.main:app --reload
```

For macOS/Linux:

```bash
MOODMIMI_ENABLE_TRANSFORMERS=0 uvicorn app.main:app --reload
```

---

## 🧪 Sample Messages

Try sending these messages to MoodMimi:

```text
I feel so tired and alone today.
```

```text
I am so proud of myself right now!
```

```text
Why is this so confusing? I don't get it.
```

```text
This is so unfair and I am really mad.
```

---

## 🎯 Project Purpose

The purpose of MoodMimi is to demonstrate how **Affective Computing** can be integrated into chatbot systems to create emotionally aware digital interactions.

This prototype combines concepts from:

- Artificial Intelligence  
- Natural Language Processing  
- Emotion Detection  
- Human-Computer Interaction  
- Mental Health Technology  
- Affective Computing  

MoodMimi shows how modern computing trends can be applied to build systems that are not only functional, but also more sensitive to human emotions.

---

## 🔮 Future Improvements

- Add voice-based tone detection  
- Add user accounts  
- Add emotion trend charts  
- Improve mascot animations  
- Add journaling features  
- Add multilingual emotion detection  
- Improve chatbot response generation  
- Deploy the application online  

---

## 👩‍💻 Developer

**Jashlein Leanne T. Marquez**  
BS Computer Science  
Polytechnic University of the Philippines  

---

## 📚 Subject

**Current Trends and Topics in Computing**

Project Focus:

```text
Affective Computing
Emotion Detection
Human-Centered AI
Chatbot Prototype
```

---

## ⚠️ Disclaimer

MoodMimi is a school project and software prototype. It is designed for educational and demonstration purposes only.

It should not be used as a replacement for professional mental health support, therapy, counseling, or medical advice.

---

<div align="center">

### 🌼 MoodMimi  
#### Helping users understand emotions, one message at a time.

</div>
````
