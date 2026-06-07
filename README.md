# TrustMail — Email Intelligence Tool

> AI-powered email verification that helps job/internship seekers and general users detect fake, spam, and suspicious email addresses before it's too late.

---

## What It Does

TrustMail analyzes any email address across four layers of intelligence:

| Check | Description |
|-------|-------------|
| ✅ Format Validation | Verifies correct email syntax and structure |
| 🌐 Domain Reputation | Detects free providers, lookalike domains, and unknown senders |
| 📬 MX Record Analysis | Checks whether the domain can actually send/receive emails |
| 🤖 AI Scam Detection | Identifies fake recruiters, phishing patterns, and suspicious signals |

A final **Trust Score (0–100)** and verdict — `Safe`, `Suspicious`, or `Dangerous` — is generated for every scan.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| AI Engine | Google Gemini 3.5 Flash (`gemini-3.5-flash`) |
| Frontend | HTML, CSS, Vanilla JS |
| Environment | python-dotenv |

---

## Getting Started

### Prerequisites
- Python 3.8+
- A free Google Gemini API key → [Get it here](https://aistudio.google.com)

---

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/trustmail.git
cd trustmail
```

### 2. Create a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Your Gemini API Key

Create your `.env` file from the template:
```bash
cp .env.example .env
```

Open `.env` and add your key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

> **How to get a free Gemini API key:**
> 1. Visit [Google AI Studio](https://aistudio.google.com)
> 2. Sign in with your Google account
> 3. Click **"Get API Key"** → **"Create API Key"**
> 4. Copy and paste it into your `.env` file

### 5. Run the App
```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## Project Structure

```
trustmail/
├── app.py                  # Flask backend — handles API calls to Gemini
├── requirements.txt        # Python dependencies
├── .env                    # Your Gemini API key (never commit this)
├── .env.example            # Safe template to share publicly
├── .gitignore              # Excludes .env from Git
└── templates/
    └── index.html          # Frontend UI
```

---

## Security

- 🔐 The Gemini API key is stored in `.env` only — **never exposed to the browser**
- 🚫 `.env` is in `.gitignore` — it will **never be pushed to GitHub**
- 🔁 All API calls are made **server-side via Flask** — the frontend only talks to your local server

---

## How It Works

```
Browser  →  POST /analyze  →  Flask  →  Gemini API
                                ↓
                         JSON response
                                ↓
Browser  ←  Trust Score + Verdict + Flags
```

---

## License

MIT License — free to use, modify, and distribute.
