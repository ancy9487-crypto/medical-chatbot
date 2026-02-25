import os
import streamlit as st
from groq import Groq

# 1. Professional UI Setup
st.set_page_config(page_title="Medical AI Assistant", page_icon="⚕️", layout="centered")
st.title("⚕️ MediBot: Medical AI")
st.markdown("""
*Disclaimer: This AI is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.*
""")

# 2. Secure Sidebar for API Key
# Replace the sidebar code with this:
import os
import streamlit as st
from groq import Groq

# This looks for the secret you just saved in the dashboard
api_key = st.secrets.get("GROQ_API_KEY")

if api_key:
    client = Groq(api_key=api_key)
    # ... rest of your chat logic ...
else:
    st.error("API Key not found in Secrets!")
# 3. Chat Logic
if user_api_key:
    client = Groq(api_key=user_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful medical assistant. Use professional terminology but explain it simply for patients. Always recommend seeing a doctor for serious symptoms."}
        ]

    # Display chat history
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask a medical question (e.g., Symptoms of seasonal allergies)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Using Llama 3 70B - Very high medical accuracy
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(completion)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("Please enter your Groq API Key in the sidebar to begin.")
