import streamlit as st
import json
import os

POEMS_FILE = "poems.json"

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.title("作品を投稿する")

title = st.text_input("タイトル")
author = st.text_input("作者名")
body = st.text_area("本文", height=250)
delete_key = st.text_input("削除キー", type="password")

if st.button("投稿する"):
    if not title or not body or not delete_key:
        st.error("すべて必須です")
    else:
        poems = load_json(POEMS_FILE, [])
        new_id = max([p["id"] for p in poems]) + 1 if poems else 1

        poems.append({
            "id": new_id,
            "title": title,
            "author": author if author else "匿名",
            "body": body,
            "delete_key": delete_key
        })

        save_json(POEMS_FILE, poems)
        st.success("投稿しました！")
