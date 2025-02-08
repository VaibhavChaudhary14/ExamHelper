import streamlit as st
import requests

# ✅ Ensure set_page_config is the first Streamlit command
st.set_page_config(page_title="AI Study Assistant", page_icon="🤖", layout="wide")

# Load API key from secrets
API_KEY = st.secrets["deepseek"]["api_key"]
API_URL = "https://api.deepseek.com/v1/chat/completions"  # Adjust if needed

def get_ai_response(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",  # Change this based on available models
        "messages": [{"role": "user", "content": user_input}]
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.json()}"

def show():
    st.header("🤖 AI Study Assistant")

    # Chat UI Styling
    st.markdown("""
    <style>
    .user-message { background-color: #FF4B4B; color: white; padding: 15px; border-radius: 15px; margin: 5px 0; }
    .assistant-message { background-color: #F0F2F6; color: #262730; padding: 15px; border-radius: 15px; margin: 5px 0; border-left: 5px solid #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

    # Display chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

    # Chat input
    with st.container():
        st.write("---")
        message = st.text_area("Ask anything about exam preparation, study tips, or personal development:", 
                               height=100,
                               placeholder="e.g., 'Can you suggest a study plan for GATE Computer Science?'")
        
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("Send 📤", use_container_width=True):
                if message:
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": message})
                    
                    # Get AI response
                    with st.spinner("Thinking..."):
                        response = get_ai_response(message)
                        st.session_state.messages.append({"role": "assistant", "content": response})

show()
