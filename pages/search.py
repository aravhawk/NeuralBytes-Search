import streamlit as st
from openai import OpenAI

if st.query_params['q'].strip(" ") is not None:
    query = st.query_params['q']

    st.set_page_config(
        page_title=f"{query} - NeuralBytes Search",
        page_icon=":mag:",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get help': 'mailto:support@neuralbytes.net?subject=Need%20Help%20with%20NeuralBytes%20Search',
            'Report a bug': 'mailto:bugs@neuralbytes.net?subject=NeuralBytes%20Search%20Bug%20Report',
            'About': '''### NeuralBytes Search: The open-source AI "search engine". Controlled by you. Owned by you. No big-tech spying. \n
            https://neuralbytes-search.streamlit.app'''
        }
    )

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    tokens_limit = 500

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    sys_prompt = f"""You are the NeuralBytes Search Bot, a ChatGPT-3.5-based AI assistant, mainly functioning as a search
    engine. IMPORTANT: DO NOT TRY BOLDING, ITALICIZING, APPLYING SPECIAL FONTS, EFFECTS, ETC. TO TEXT. DON'T PUT _<TEXT>_
    *<TEXT>* `<TEXT>` OR ANYTHING SIMILAR, AS THE STREAMLIT WEB INTERFACE HATES (SUCKS AT) WORKING WITH TEXT FORMATTING AND 
    MARKDOWN. ALSO, MAX TOKENS FOR RESPONSE: {tokens_limit}"""

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.session_state["messages"].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
                model='gpt-3.5-turbo-0125',
                messages=[
                             {"role": "system", "content": sys_prompt}
                         ] +
                         [
                             {"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]
                         ],
                stream=True,
                max_tokens=tokens_limit
        ):
            incremental_content = response.choices[0].delta.content or ""
            full_response += incremental_content
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state["messages"].append({"role": "assistant", "content": full_response})
else:
    st.stop()
