import streamlit as st
import json
import os

MESSAGES_FILE = "messages.json"
POEMS_FILE = "poems.json"

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

st.title("作者用スレッド一覧")

poems = load_json(POEMS_FILE, [])
messages = load_json(MESSAGES_FILE, [])

authors = list(set([p["author"] for p in poems]))

author = st.selectbox("作者名を選択", authors)
if not author:
    st.stop()

author_threads = [t for t in messages if author in t["participants"]]

for t in author_threads:
    other = [p for p in t["participants"] if p != author][0]

    if st.button(f"{other} さんとのチャット", key=f"author_thread_{t['thread_id']}"):
        st.session_state["role"] = "author"
        st.session_state["selected_thread_id"] = t["thread_id"]

        if "viewer_name" in st.session_state:
            del st.session_state["viewer_name"]
        if "selected_poem_id" in st.session_state:
            del st.session_state["selected_poem_id"]

        st.switch_page("pages/3_チャット.py")
