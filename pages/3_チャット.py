import streamlit as st
import json
import os

POEMS_FILE = "poems.json"
MESSAGES_FILE = "messages.json"

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.title("チャットルーム")

poems = load_json(POEMS_FILE, [])
messages = load_json(MESSAGES_FILE, [])

# 作者 or 閲覧者のどちらかが thread_id を持っている
thread_id = st.session_state.get("selected_thread_id", None)

# 閲覧者の場合は poem_id から thread を探す
if thread_id is None:
    poem_id = st.session_state.get("selected_poem_id", None)
    if poem_id is None:
        st.error("作品が選択されていません")
        st.stop()

    poem = next((p for p in poems if p["id"] == poem_id), None)
    if poem is None:
        st.error("作品が見つかりません")
        st.stop()

    st.subheader(f"作品：{poem['title']}（作者：{poem['author']}）")

    username = st.text_input("あなたの名前（チャットで表示）")
    if not username:
        st.stop()

    # 1対1スレッドを検索
    thread = next(
        (t for t in messages 
         if t["poem_id"] == poem_id and username in t["participants"]),
        None
    )

    # なければ新規作成
    if thread is None:
        new_thread_id = max([t["thread_id"] for t in messages], default=0) + 1
        thread = {
            "thread_id": new_thread_id,
            "poem_id": poem_id,
            "participants": [poem["author"], username],
            "messages": []
        }
        messages.append(thread)
        save_json(MESSAGES_FILE, messages)

    thread_id = thread["thread_id"]
    st.session_state["selected_thread_id"] = thread_id

else:
    # 作者がスレッド一覧から来た場合
    thread = next((t for t in messages if t["thread_id"] == thread_id), None)
    if thread is None:
        st.error("スレッドが見つかりません")
        st.stop()

    poem = next((p for p in poems if p["id"] == thread["poem_id"]), None)
    st.subheader(f"作品：{poem['title']}（作者：{poem['author']}）")

    # 作者は自動的に作者名
    username = poem["author"]

# CSS
st.markdown("""
<style>
.chat-container {
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 10px;
}

.chat-left {
    background-color: #ffffff;
    color: black;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px;
    max-width: 60%;
}

.chat-right {
    background-color: #4da3ff;
    color: white;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px;
    margin-left: auto;
    max-width: 60%;
}

.read-label {
    font-size: 10px;
    color: #555;
    margin-left: auto;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

st.write("### メッセージ")
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# 未読通知
other = [p for p in thread["participants"] if p != username][0]
unread_count = sum(
    1 for msg in thread["messages"]
    if msg["from"] == other and not msg.get("read", False)
)

if unread_count > 0:
    st.warning(f"📩 {other} さんからの新着メッセージがあります")

# メッセージ表示
for i, msg in enumerate(thread["messages"]):

    # 自分以外のメッセージは既読にする
    if msg["from"] != username and not msg.get("read", False):
        msg["read"] = True
        save_json(MESSAGES_FILE, messages)

    # 作者（左）
    if msg["from"] == poem["author"]:
        st.markdown(
            f"<div class='chat-left'><b>{msg['from']}</b><br>{msg['text']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-right'><b>{msg['from']}</b><br>{msg['text']}</div>",
            unsafe_allow_html=True
        )

    # 自分のメッセージだけ削除可能
    if msg["from"] == username:
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("削除", key=f"del_{i}"):
                thread["messages"].pop(i)
                save_json(MESSAGES_FILE, messages)
                st.rerun()

        with col2:
            if msg.get("read", False):
                st.markdown("<div class='read-label'>既読</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# メッセージ送信
new_msg = st.text_input("メッセージを入力")

if st.button("送信"):
    if new_msg.strip():
        thread["messages"].append({
            "from": username,
            "text": new_msg,
            "read": False
        })
        save_json(MESSAGES_FILE, messages)
        st.rerun()
