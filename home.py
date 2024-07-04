import streamlit as st

st.set_page_config(
    page_title=f"NeuralBytes Search",
    page_icon=":mag:",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get help': 'mailto:support@neuralbytes.net?subject=Need%20Help%20with%20NeuralBytes%20Search',
        'Report a bug': 'mailto:bugs@neuralbytes.net?subject=NeuralBytes%20Search%20Bug%20Report',
        'About': '''### NeuralBytes Search: The open-source AI "search engine". Controlled by you. Owned by you. No big-tech spying. \n
        https://neuralbytes-search.streamlit.app'''
    }
)

st.title("NeuralBytes Search")
st.write('The open-source AI "search engine". Controlled by you. Owned by you. No big-tech spying.')
st.write("[Help improve NeuralBytes Search](mailto:feedback@neuralbytes.net?subject=AlphaPredict%20Feedback)")

query = st.text_input("What would you like to know?")
st.page_link(f"https://neuralbytes-search.streamlit.app/search?q={query}", label="Search", icon="🔍", disabled=False)
