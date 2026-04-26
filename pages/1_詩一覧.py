import streamlit as st
import json

POEMS_FILE = "poems.json"

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

st.title("作品一覧")

poems = load_json(POEMS_FILE, [])

for poem in poems:
    with st.container(border=True):
        st.subheader(poem["title"])
        st.write(f"作者：{poem['author']}")
        st.write("---")
        st.write(poem["body"])

        if st.button(f"興味があります（ID: {poem['id']}）", key=f"interest_{poem['id']}"):
            st.session_state["selected_poem_id"] = poem["id"]
            st.switch_page("pages/3_チャット.py")
