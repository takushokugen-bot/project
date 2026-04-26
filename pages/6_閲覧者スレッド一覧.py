import streamlit as st
import json
import os

MESSAGES_FILE = "messages.json"

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

st.title("閲覧者用スレッド一覧")

messages = load_json(MESSAGES_FILE, [])

viewer_name = st.text_input("あなたの名前（チャットで使った名前）")
if not viewer_name:
    st.stop()

viewer_threads = [t for t in messages if viewer_name in t["participants"]]

for t in viewer_threads:
    other = [p for p in t["participants"] if p != viewer_name][0]

    if st.button(f"{other} さんとのチャット", key=f"viewer_thread_{t['thread_id']}"):
        st.session_state["role"] = "viewer"
        st.session_state["viewer_name"] = viewer_name
        st.session_state["selected_thread_id"] = t["thread_id"]

        if "selected_poem_id" in st.session_state:
            del st.session_state["selected_poem_id"]

        st.switch_page("pages/3_チャット.py")
