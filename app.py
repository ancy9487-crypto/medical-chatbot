import streamlit as st
import os

# 1. Try to import Groq, if it fails, show a helpful message
try:
    from groq import Groq
except ImportError:
    st.error("The 'groq' library is not installed. Please check your requirements.txt file in GitHub.")
    st.stop()

st.set_page_config(page_title="Medical Bot", page_icon="⚕️")

# 2. Check for API Key in Secrets OR Sidebar
api_key = st.secrets.get("GROQ_API_KEY") or st.sidebar.text_input("Paste Groq API Key here", type="password")

if not api_key:
    st.warning("Please provide a Groq API Key to start.")
    st.stop()

try:
    client = Groq(api_key=api_key)
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a medical assistant."}]

    for msg in st.session_state.messages[1:]:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Call the AI
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.messages,
        )
        
        response = completion.choices[0].message.content
        st.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

except Exception as e:
    st.error(f"An error occurred: {e}")
