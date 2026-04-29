const landingPage = document.querySelector("#landingPage");
const chatApp = document.querySelector("#chatApp");
const heroTalkBtn = document.querySelector("#heroTalkBtn");
const navTalkBtn = document.querySelector("#navTalkBtn");
const previewBtn = document.querySelector("#previewBtn");
const backToLandingBtn = document.querySelector("#backToLandingBtn");
const chatForm = document.querySelector("#chatForm");
const messageInput = document.querySelector("#messageInput");
const chatWindow = document.querySelector("#chatWindow");
const sendBtn = document.querySelector("#sendBtn");
const mascot = document.querySelector("#mascot");
const mascotEmoji = document.querySelector("#mascotEmoji");
const emotionName = document.querySelector("#emotionName");
const confidenceText = document.querySelector("#confidenceText");
const confidenceBar = document.querySelector("#confidenceBar");
const toneText = document.querySelector("#toneText");
const suggestionText = document.querySelector("#suggestionText");
const scoreList = document.querySelector("#scoreList");
const moodBars = document.querySelector("#moodBars");
const modelBadge = document.querySelector("#modelBadge");
const clearHistoryBtn = document.querySelector("#clearHistoryBtn");

const sessionId = getOrCreateSessionId();

function showChat() {
  landingPage.classList.add("app-hidden");
  chatApp.classList.remove("app-hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
  setTimeout(() => messageInput.focus(), 250);
}

function showLanding() {
  chatApp.classList.add("app-hidden");
  landingPage.classList.remove("app-hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
}


const emotionMeta = {
  Happiness: { emoji: "😄", className: "happiness" },
  Sadness: { emoji: "🥺", className: "sadness" },
  Anger: { emoji: "😤", className: "anger" },
  Fear: { emoji: "😟", className: "fear" },
  Love: { emoji: "🥰", className: "love" },
  Surprise: { emoji: "😮", className: "surprise" },
  Disgust: { emoji: "😖", className: "disgust" },
  Confusion: { emoji: "🤔", className: "confusion" },
  Desire: { emoji: "✨", className: "desire" },
  Guilt: { emoji: "😔", className: "guilt" },
  Sarcasm: { emoji: "🙃", className: "sarcasm" },
  Shame: { emoji: "🫣", className: "shame" },
  Neutral: { emoji: "🙂", className: "neutral" },
  Crisis: { emoji: "🧡", className: "crisis" },
};

function getOrCreateSessionId() {
  const key = "moodmimi_session_id";
  let value = localStorage.getItem(key);
  if (!value) {
    value = `session-${Date.now()}-${Math.random().toString(16).slice(2)}`;
    localStorage.setItem(key, value);
  }
  return value;
}

function escapeHTML(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function addMessage(role, text, options = {}) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role === "user" ? "user-message" : "bot-message"}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "🧑" : "💛";

  const bubble = document.createElement("div");
  bubble.className = `bubble ${options.crisis ? "crisis-card" : ""}`;
  bubble.innerHTML = `<p>${escapeHTML(text)}</p>`;

  if (options.meta) {
    bubble.innerHTML += `<small>${escapeHTML(options.meta)}</small>`;
  }

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);
  chatWindow.appendChild(wrapper);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function setLoading(isLoading) {
  sendBtn.disabled = isLoading;
  messageInput.disabled = isLoading;
  sendBtn.textContent = isLoading ? "Thinking..." : "Send";
}

async function sendMessage(message) {
  const text = message.trim();
  if (!text) return;

  addMessage("user", text);
  messageInput.value = "";
  setLoading(true);

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, session_id: sessionId }),
    });

    if (!response.ok) {
      const errorPayload = await response.json().catch(() => ({}));
      throw new Error(errorPayload.detail || "MoodMimi could not process the message.");
    }

    const data = await response.json();
    addMessage("bot", data.reply, {
      crisis: data.is_crisis,
      meta: `${data.emotion} · ${Math.round(data.confidence * 100)}% confidence`,
    });
    updateEmotionPanel(data);
    await loadHistory();
  } catch (error) {
    addMessage("bot", `Sorry, I ran into an app error: ${error.message}`);
  } finally {
    setLoading(false);
    messageInput.focus();
  }
}

function updateEmotionPanel(data) {
  const emotion = data.emotion || "Neutral";
  const meta = emotionMeta[emotion] || emotionMeta.Neutral;
  const percent = Math.max(0, Math.min(100, Math.round((data.confidence || 0) * 100)));

  mascot.className = `mascot ${meta.className}`;
  mascotEmoji.textContent = meta.emoji;
  emotionName.textContent = emotion;
  confidenceText.textContent = `${percent}%`;
  confidenceBar.style.width = `${percent}%`;
  toneText.textContent = data.tone || "No tone details available.";
  suggestionText.textContent = data.suggestion || "No suggestion available.";
  modelBadge.textContent = data.model_used || "model unknown";

  const scores = Array.isArray(data.scores) ? data.scores : [];
  scoreList.innerHTML = scores.map((item) => {
    const scorePercent = Math.max(0, Math.min(100, Math.round((item.score || 0) * 100)));
    return `
      <div class="score-row">
        <span>${escapeHTML(item.label)}</span>
        <div class="score-meter"><div class="score-fill" style="width: ${scorePercent}%"></div></div>
        <strong>${scorePercent}%</strong>
      </div>
    `;
  }).join("");
}

async function checkHealth() {
  try {
    const response = await fetch("/api/health");
    const data = await response.json();
    if (data.model_loaded) {
      modelBadge.textContent = data.model_used;
    } else {
      modelBadge.textContent = "keyword-fallback";
    }
  } catch {
    modelBadge.textContent = "offline";
  }
}

async function loadHistory() {
  try {
    const response = await fetch("/api/history?limit=100");
    const data = await response.json();
    const items = Array.isArray(data.items) ? data.items : [];
    renderMoodBars(items);
  } catch {
    moodBars.className = "mood-bars empty";
    moodBars.textContent = "Could not load history.";
  }
}

function renderMoodBars(items) {
  const counts = {};
  for (const item of items) {
    counts[item.emotion] = (counts[item.emotion] || 0) + 1;
  }

  const entries = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  if (entries.length === 0) {
    moodBars.className = "mood-bars empty";
    moodBars.textContent = "No history yet.";
    return;
  }

  moodBars.className = "mood-bars";
  const max = Math.max(...entries.map((entry) => entry[1]));
  moodBars.innerHTML = entries.map(([emotion, count]) => {
    const width = Math.max(8, Math.round((count / max) * 100));
    return `
      <div class="mood-row">
        <span>${escapeHTML(emotion)}</span>
        <div class="mood-track"><div class="mood-fill" style="width: ${width}%"></div></div>
        <strong>${count}</strong>
      </div>
    `;
  }).join("");
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(messageInput.value);
});

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => {
    sendMessage(button.dataset.prompt || "");
  });
});

clearHistoryBtn.addEventListener("click", async () => {
  const confirmed = window.confirm("Clear MoodMimi chat history from SQLite?");
  if (!confirmed) return;

  await fetch("/api/history", { method: "DELETE" });
  await loadHistory();
});

[heroTalkBtn, navTalkBtn].forEach((button) => {
  button.addEventListener("click", showChat);
});

previewBtn.addEventListener("click", () => {
  document.querySelector("#howItWorks").scrollIntoView({ behavior: "smooth" });
});

backToLandingBtn.addEventListener("click", showLanding);

checkHealth();
loadHistory();
