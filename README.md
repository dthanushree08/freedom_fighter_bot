# Freedom Fighters Chatbot (Retrieval based)

A small chatbot that only answers questions about 10 Indian freedom fighters
(Gandhi, Bhagat Singh, Subhas Chandra Bose, Rani Lakshmibai, Sardar Patel,
Chandrashekhar Azad, Lala Lajpat Rai, Bal Gangadhar Tilak, Sarojini Naidu,
Jawaharlal Nehru). It works by searching a small CSV knowledge base with
TF-IDF + cosine similarity - no paid API, no OpenAI key needed.

## Files in this project

```
freedom-fighters-bot/
├── app.py                  <- the streamlit app (chatbot logic + UI)
├── requirements.txt        <- python packages needed
├── data/
│   └── knowledge_base.csv  <- the facts the bot searches through
└── README.md
```

These are the only 3 files (+ folder) you need. Nothing else.

---

## PART A - Push the project to GitHub

**Step 1: Create a GitHub account (skip if you have one)**
Go to https://github.com and sign up.

✅ Check: you can log in and see your dashboard.

**Step 2: Create a new repository**
- Click the "+" icon top right → "New repository"
- Name it something like `freedom-fighters-bot`
- Keep it Public (Streamlit Cloud free tier needs public repo, or a linked private one)
- Do NOT initialize with a README (we already have our own files)
- Click "Create repository"

✅ Check: GitHub shows you an empty repo page with a URL like
`https://github.com/yourusername/freedom-fighters-bot`

**Step 3: Upload the files**
Easiest way if you're not comfortable with git commands:
- On the empty repo page, click "uploading an existing file"
- Drag and drop `app.py`, `requirements.txt`, and the `data` folder
  (make sure `knowledge_base.csv` ends up inside a folder literally named `data`)
- Scroll down, click "Commit changes"

(If you prefer git command line instead:)
```
git clone https://github.com/yourusername/freedom-fighters-bot.git
cd freedom-fighters-bot
# copy app.py, requirements.txt, data/ folder into this cloned folder
git add .
git commit -m "first commit - freedom fighters bot"
git push
```

✅ Check: refresh your GitHub repo page. You should see `app.py`,
`requirements.txt`, and a `data` folder containing `knowledge_base.csv`,
all sitting in the ROOT of the repo (not nested inside another folder).
This is important - Streamlit looks for `app.py` at the root by default.

---

## PART B - Deploy on Streamlit Community Cloud

**Step 4: Create a Streamlit account**
Go to https://share.streamlit.io and sign in with your GitHub account
(easiest option, one click).

✅ Check: you land on a dashboard that says "Create app" somewhere.

**Step 5: Create a new app**
- Click "Create app" → "Deploy a public app from GitHub"
- Repository: pick `yourusername/freedom-fighters-bot`
- Branch: `main` (or `master`, whatever your default branch is called)
- Main file path: `app.py`
- Click "Deploy"

✅ Check: a build log window opens and starts installing packages from
`requirements.txt`. You'll see lines like "Installing streamlit..." etc.

**Step 6: Wait for the build**
This usually takes 1-3 minutes the first time.

✅ Check: the log ends with something like "You can now view your Streamlit
app in your browser" and the app screen loads showing the title
"🇮🇳 Freedom Fighters Chatbot".

**Step 7: Test it live**
Type a question in the chat box, for example:
- "who was bhagat singh"
- "when did gandhi die"
- "what's the weather today" (should politely refuse, since it's off-topic)

✅ Check: on-topic questions return a real answer with a confidence caption,
off-topic ones return the "I don't know this topic" message. If both work,
your deployment is fully working.

**Step 8 (optional): Share it**
Streamlit gives you a public URL like
`https://yourusername-freedom-fighters-bot.streamlit.app`
You can share this link with anyone, they don't need a Streamlit account to use it.

---

## Common problems and fixes

| Problem | Likely cause | Fix |
|---|---|---|
| "File not found: data/knowledge_base.csv" | data folder not at repo root, or wrong casing | Make sure folder is named exactly `data` (lowercase) and sits next to app.py |
| App builds but shows a blank page | Wrong "Main file path" during Step 5 | Edit the app settings on Streamlit Cloud and set it to `app.py` |
| Every answer says "I don't know" | requirements didn't install properly | Check the build log for red error lines, usually a typo in requirements.txt |
| Changes I push to GitHub don't show up | Streamlit caches app data | Click "Reboot app" from the Streamlit Cloud dashboard, or just wait ~1 min, it usually auto redeploys on every git push |

---

## Wanna extend it later?
- Add more rows to `data/knowledge_base.csv` (just follow the same format: id, name, text) to teach it new people
- Swap TF-IDF for sentence-transformers embeddings if you want smarter semantic matching (needs a bigger requirements.txt though)
- Change the topic entirely - just replace the CSV with facts about anything else (movies, a company's FAQ, your own notes) and it becomes a bot for that topic
