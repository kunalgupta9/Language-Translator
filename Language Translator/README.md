# 🌐 Language Translator

Hi! I’m **Kunal**, a B.Tech CSE student.  
I built an elegant, dark-themed **AI-powered Language Translator Web App** using **Flask**, **Google Translate API**, and **gTTS (Google Text-to-Speech)**.

It supports **live translation while typing**, **text-to-speech audio**, and a **minimal modern UI** — simple yet powerful.

---

## ✨ What it does

- ⚡ **Live translation** as you type — no refresh or button press needed.  
- 🔊 **Text-to-speech:** click the small speaker icon to hear the translation.  
- 🗣️ **Auto-Speak Mode:** automatically plays translated audio for every sentence.  
- 🌍 **Auto-detect source language:** no need to manually select input language.  
- 💬 **Supports all major languages** — English, Hindi, Chinese, Korean, and many more.  
- 🎨 **Clean dark theme:** smooth gradient, responsive layout, and modern look.  

---

## 🧩 Tech I used

- **Flask** (Python) for backend  
- **googletrans** for language translation  
- **gTTS** for text-to-speech audio  
- **Vanilla HTML, CSS, JS** for frontend  

---

## 🛠️ Tech Stack

| Layer | Technology Used |
|-------|------------------|
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla JS) |
| **Backend** | Flask (Python) |
| **Translation API** | `googletrans==4.0.0rc1` |
| **Text-to-Speech (TTS)** | `gTTS==2.5.2` |
| **Styling** | Custom CSS with gradient dark theme |

---

## ⚡ Quick start

```bash
# 1) (Optional) Create a virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app
python app.py

# 4) Open in Browser
Visit http://127.0.0.1:5000
```

---

## 🖥️ How to Use

1. Select **source** and **target** languages (or leave “Auto Detect”).  
2. Type text — the translation appears instantly.  
3. Click the 🔊 **speaker icon** to listen to the translation aloud.  
4. (Optional) Enable **Auto-Speak** to automatically play each translation.  

---

## 🗂️ Project structure

```
Language Translator/
├─ app.py                  # Flask app
├─ requirements.txt        # Dependencies
├─ templates/
│  └─ index.html           # Page template
└─ static/
   ├─ style.css            # Dark theme styles
   └─ app.js               # Live translate + audio logic
```

---

## 👨‍💻 Developer

**Kunal**  
🎓 *B.Tech in Computer Science & Engineering*  
💬 “Turning ideas into reality through clean and simple code.”

---

## 📜 Note

This project was created for learning and academic purposes.  
Feel free to explore, use, or improve it. 🌟
