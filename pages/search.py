import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state["messages"] = []

sys_prompt = """You are the NeuralBytes Search Bot, a ChatGPT-3.5-based AI assistant, mainly functioning as a search
engine. IMPORTANT: DO NOT TRY BOLDING, ITALICIZING, APPLYING SPECIAL FONTS, EFFECTS, ETC. TO TEXT. DON'T PUT _<TEXT>_
*<TEXT>* `<TEXT>` OR ANYTHING SIMILAR, AS THE STREAMLIT WEB INTERFACE HATES (SUCKS AT) WORKING WITH TEXT FORMATTING AND 
MARKDOWN."""

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.query_params['q'].strip(" ") is not None:
    query = st.query_params['q']
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
                max_tokens=100
        ):
            incremental_content = response.choices[0].delta.content or ""
            full_response += incremental_content
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state["messages"].append({"role": "assistant", "content": full_response})
