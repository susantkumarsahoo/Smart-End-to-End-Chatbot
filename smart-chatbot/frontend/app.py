import streamlit as st
import requests
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Smart AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .bot-message {
        background-color: #f1f3f4;
        color: black;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🤖 Smart Chatbot")
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Messages", len(st.session_state.messages))
    
    if st.session_state.session_id:
        st.text(f"Session: {st.session_state.session_id[:8]}...")

# Main chat interface
st.title("💬 Smart AI Chatbot")
st.caption("Powered by LangChain, FastAPI & OpenAI")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "message": prompt,
                        "session_id": st.session_state.session_id
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    bot_response = data["response"]
                    st.session_state.session_id = data["session_id"]
                    
                    st.markdown(bot_response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": bot_response
                    })
                else:
                    st.error("Failed to get response from the server")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure the backend server is running on http://localhost:8000")# Streamlit UI application
