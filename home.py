import streamlit as st

st.title("NeuralBytes Search")
st.write('The open-source AI "search engine". Controlled by you. Owned by you. No big-tech spying.')

query = st.text_input("What would you like to know?")
st.page_link(f"http://localhost:8501/search?q={query}", label="Search", icon="🔎", disabled=False)
