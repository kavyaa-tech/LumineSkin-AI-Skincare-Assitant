import sys
import os
import os
os.environ.pop("SSL_CERT_FILE", None)

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.rag_chain import generate_rag_answer
import traceback
import streamlit as st

st.set_page_config(page_title="LumineSkin Chat", page_icon="💅🏻")
st.title("💅🏻 LumineSkin Skincare Assistant")
st.markdown("<h4 style='color:#c06c84;'>Welcome to LumineSkin Glow Chat °❀⋆.ೃ࿔*:･</h4>", unsafe_allow_html=True)
st.markdown("Ask me anything about your skin, I'm here to help you shine 🌟")
st.markdown("<h7>📝 Disclaimer: This assistant offers general skincare info. For medical advice, please consult a dermatologist.</h7>", unsafe_allow_html=True)


# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.chat_input("Ask your skincare question...")

if user_input:
    # Display user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Get bot response
    with st.spinner("LumineSkin is thinking..."):
        try:
            response = generate_rag_answer(user_input)
        except Exception as e:
            response = f"Error: {e}"

    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Display conversation
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])