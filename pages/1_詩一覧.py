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

            # ★ 閲覧者として入る
            st.session_state["role"] = "viewer"

            # ★ どの作品か
            st.session_state["selected_poem_id"] = poem["id"]

            # ★ 新規スレッドを作る可能性があるので thread_id は消す
            st.session_state["selected_thread_id"] = None

            # ★ 閲覧者名はまだ入力していないので消す
            if "viewer_name" in st.session_state:
                del st.session_state["viewer_name"]

            st.switch_page("pages/3_チャット.py")
