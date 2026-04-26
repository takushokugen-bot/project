import streamlit as st
import json
import os

POEMS_FILE = "poems.json"
MESSAGES_FILE = "messages.json"

# =========================================================
# JSON 読み書き
# =========================================================
def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# =========================================================
# データ読み込み
# =========================================================
poems = load_json(POEMS_FILE, [])
messages = load_json(MESSAGES_FILE, [])

st.title("チャットルーム")

# =========================================================
# 必須の状態を取得
# =========================================================
role = st.session_state.get("role", None)
thread_id = st.session_state.get("selected_thread_id", None)
poem_id = st.session_state.get("selected_poem_id", None)

# =========================================================
# ★ role が無い＝絶対に壊れるので即停止
# =========================================================
if role not in ["viewer", "author"]:
    st.error("このページは一覧から開いてください。（role が設定されていません）")
    st.stop()

# =========================================================
# ① 閲覧者（作品ページから来た） → thread_id がまだ無い
# =========================================================
if role == "viewer" and thread_id is None:

    if poem_id is None:
        st.error("作品が選択されていません")
        st.stop()

    poem = next((p for p in poems if p["id"] == poem_id), None)
    if poem is None:
        st.error("作品データが壊れています")
        st.stop()

    st.subheader(f"作品：{poem['title']}（作者：{poem['author']}）")

    # ★ viewer_name の扱いを完全に安定化
    username = st.session_state.get("viewer_name", "")

    if not username:
        username = st.text_input("あなたの名前（チャットで表示）")
        if username:
            st.session_state["viewer_name"] = username
        else:
            st.stop()

    # 既存スレッド検索
    thread = next(
        (t for t in messages
         if t["poem_id"] == poem_id and username in t["participants"]),
        None
    )

    # なければ作成
    if thread is None:
        new_id = max([t["thread_id"] for t in messages], default=0) + 1
        thread = {
            "thread_id": new_id,
            "poem_id": poem_id,
            "participants": [poem["author"], username],
            "messages": []
        }
        messages.append(thread)
        save_json(MESSAGES_FILE, messages)

    # thread_id を確定
    st.session_state["selected_thread_id"] = thread["thread_id"]
    thread_id = thread["thread_id"]

# =========================================================
# ② 作者 or 閲覧者スレッド一覧から来た
# =========================================================
thread = next((t for t in messages if t["thread_id"] == thread_id), None)
if thread is None:
    st.error("スレッドが見つかりません")
    st.stop()

poem = next((p for p in poems if p["id"] == thread["poem_id"]), None)
if poem is None:
    st.error("作品データが壊れています")
    st.stop()

st.subheader(f"作品：{poem['title']}（作者：{poem['author']}）")

# =========================================================
# ★ 役割に応じて名前を決定（絶対に壊れない形）
# =========================================================
if role == "author":
    username = poem["author"]

elif role == "viewer":
    username = st.session_state.get("viewer_name", "")
    if not username:
        st.error("閲覧者名が取得できませんでした（viewer_name がありません）")
        st.stop()

else:
    st.error("role が不正です。ページを一覧から開き直してください。")
    st.stop()

# =========================================================
# メッセージ表示
# =========================================================
st.write("### メッセージ")

for msg in thread["messages"]:
    st.write(f"{msg['from']}：{msg['text']}")

# =========================================================
# メッセージ送信
# =========================================================
new_msg = st.text_input("メッセージを入力", key="chat_message")

if st.button("送信"):
    if new_msg.strip():
        thread["messages"].append({
            "from": username,
            "text": new_msg,
            "read": False
        })
        save_json(MESSAGES_FILE, messages)
        st.rerun()
