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

st.title("作品を削除する")

poems = load_json(POEMS_FILE, [])

for p in poems:
    st.write(f"ID: {p['id']} / {p['title']}")

delete_id = st.number_input("削除ID", min_value=1, step=1)
delete_key = st.text_input("削除キー", type="password")

if st.button("削除"):
    target = next((p for p in poems if p["id"] == delete_id), None)

    if target is None:
        st.error("作品がありません")
    elif target["delete_key"] != delete_key:
        st.error("削除キーが違います")
    else:
        poems = [p for p in poems if p["id"] != delete_id]
        save_json(POEMS_FILE, poems)
        st.success("削除しました")
