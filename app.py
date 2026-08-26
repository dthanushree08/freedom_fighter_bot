"""
Freedom Fighters Chatbot - a simple retrieval based Q&A bot.

Idea is simple: we keep a small csv of facts about Indian freedom fighters,
turn every row into a TF-IDF vector, and when the user asks something we
turn their question into a vector too and find the closest matching rows
using cosine similarity. No LLM API needed, works fully offline, free to
host on Streamlit Cloud.

If the question is too far off from anything in our data (low similarity
score) we just tell the user this bot only knows about freedom fighters,
instead of making something up.
"""

import os
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---- basic page setup ----
st.set_page_config(page_title="Freedom Fighters Bot", page_icon="🇮🇳")
st.title("🇮🇳 Freedom Fighters Chatbot")
st.caption("Ask me about Gandhi, Bhagat Singh, Netaji, Rani Lakshmibai and other Indian freedom fighters. I only know this topic, so don't ask me about cricket scores 😄")

# Build the path relative to THIS file's own folder, not the current working
# directory. Streamlit Cloud doesn't always run the app from the repo root,
# so a plain "data/knowledge_base.csv" string can silently fail there even
# though it works fine on your own laptop.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(APP_DIR, "data", "knowledge_base.csv")
SIMILARITY_CUTOFF = 0.12  # below this, we say "I don't know" instead of guessing


@st.cache_resource
def load_and_fit():
    if not os.path.exists(DATA_PATH):
        st.error(
            f"Couldn't find the knowledge base file at:\n\n`{DATA_PATH}`\n\n"
            "This usually means the `data` folder wasn't uploaded to GitHub "
            "next to app.py, or it's nested one level too deep. "
            "Check your repo and make sure `data/knowledge_base.csv` "
            "sits right beside app.py at the repo root."
        )
        st.stop()
    df = pd.read_csv(DATA_PATH)
    # trick: repeat the person's name a couple of times before the text so
    # that a direct name match in the question weighs more than a name that
    # just happens to be mentioned inside someone else's paragraph
    boosted_text = (df["name"] + " " + df["name"] + " " + df["text"])
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(boosted_text)
    return df, vectorizer, matrix


df, vectorizer, doc_matrix = load_and_fit()


def get_answer(user_question, top_k=2):
    q_vec = vectorizer.transform([user_question])
    scores = cosine_similarity(q_vec, doc_matrix).flatten()

    best_idx = scores.argsort()[::-1][:top_k]
    best_score = scores[best_idx[0]]

    if best_score < SIMILARITY_CUTOFF:
        return None, best_score

    rows = df.iloc[best_idx]
    return rows, best_score


# ---- chat history so it feels like a real chat, not a single search box ----
if "history" not in st.session_state:
    st.session_state.history = []

for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.write(msg)

user_q = st.chat_input("Ask something about an Indian freedom fighter...")

if user_q:
    st.session_state.history.append(("user", user_q))
    with st.chat_message("user"):
        st.write(user_q)

    rows, score = get_answer(user_q)

    with st.chat_message("assistant"):
        if rows is None:
            reply = ("Hmm, that doesn't seem related to Indian freedom fighters, "
                      "which is the only thing I've been trained to answer. "
                      "Try asking me about Gandhi, Bhagat Singh, Netaji, Rani Lakshmibai, "
                      "Sardar Patel and a few others.")
            st.write(reply)
        else:
            # combine the top matching chunks into one answer
            name = rows.iloc[0]["name"]
            reply_parts = [r["text"] for _, r in rows.iterrows()]
            reply = f"**About {name}:**\n\n" + "\n\n".join(reply_parts)
            st.write(reply)
            st.caption(f"(match confidence: {score:.2f})")

    st.session_state.history.append(("assistant", reply))

with st.sidebar:
    st.header("About this bot")
    st.write(
        "This is a retrieval based chatbot - it does not generate new text, "
        "it only searches through a small hand written knowledge base and "
        "returns the closest matching facts. Currently it knows about 10 "
        "Indian freedom fighters."
    )
    if st.button("Clear chat"):
        st.session_state.history = []
        st.rerun()
