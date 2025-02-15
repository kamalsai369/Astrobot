import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="You are an expert AstroPhysicist. Provide concise, correct solutions with strategic topics about cosmology, theorems, and problems. Always respond in English.",
)

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Streamlit UI
st.title("Astrophysics Chatbot:man-tipping-hand:")
# st.write("Welcome to the Astrophysics  Chatbot! Ask me anything about the universe, cosmology, or astrophysics.")
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["GEMINI 2.0 Flash"],
        index=0
    )
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
    -  query Solutions
    -  Solution Design
    -  Mathematical Proofs
    -  Theory Explanation
    """)
    st.divider()
    st.markdown("Built with [GEMINI](https://aistudio.google.com/) ")
# Display chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask your question about astrophysics or cosmology:")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get chatbot response
    response = st.session_state.chat_session.send_message(user_input)
    chatbot_response = response.text

    # Add chatbot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
    with st.chat_message("assistant"):
        st.markdown(chatbot_response)