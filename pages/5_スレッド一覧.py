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

# 作者名を取得（作品から）
authors = list(set([p["author"] for p in poems]))

st.write("作者名を選択してください")
author = st.selectbox("作者", authors)

if not author:
    st.stop()

st.write("### あなた宛のスレッド一覧")

# 作者が参加しているスレッドだけ抽出
author_threads = [
    t for t in messages if author in t["participants"]
]

if not author_threads:
    st.info("まだスレッドがありません")
    st.stop()

for t in author_threads:
    # 相手の名前を取得
    other = [p for p in t["participants"] if p != author][0]

    # 未読数
    unread = sum(
        1 for m in t["messages"]
        if m["from"] == other and not m.get("read", False)
    )

    label = f"{other} さんとのチャット"
    if unread > 0:
        label += f"（未読 {unread}）"

    if st.button(label, key=f"thread_{t['thread_id']}"):
        st.session_state["selected_thread_id"] = t["thread_id"]
        st.switch_page("pages/3_チャット.py")
