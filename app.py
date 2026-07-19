import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

st.set_page_config(
    page_title="ChatVerse AI",
    page_icon="🎭"
)

st.title("🤖 THE MULTIVERSE OF CHATBOTS")

personality = st.selectbox(
    "Who do you want to talk to?",
    [
        "💻 Coding Mentor",
        "😂 Funny Comedian",
        "🏴‍☠️ Pirate",
        "🧙 Wise Wizard",
        "⚽ Ronaldo Crazy Fan",
        "😡 Angry Ravi Shastri",
        "🩺 Doctor",
        "💼 Interviewer",
        "🕵️ Sherlock Holmes",
        "🦇 Batman",
        "🕷️ Spider-Man",
        "⚡ Iron Man",
        "🧘 Lord Krishna",
        "👑 Chhatrapati Shivaji Maharaj",
        "🎤 Motivational Speaker",
        "📚 College Professor",
        "🤖 AI Assistant",
        "🎬 Movie Critic",
        "🍳 Master Chef",
        "✈️ Travel Guide",
        "💪 Fitness Coach",
        "💰 Financial Advisor",
        "👻 Horror Story Teller",
        "🎮 Gamer",
        "📖 Story Writer"
    ]
)

response_length = st.selectbox(
    "Response Length",
    [
        "Short",
        "Medium",
        "Long"
    ]
)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear Chat
if st.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if user_message := st.chat_input("Say something..."):

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    conversation = ""

    for message in st.session_state.messages:
        if message["role"] == "user":
            conversation += f"User: {message['content']}\n"
        else:
            conversation += f"AI: {message['content']}\n"

    ai_instruction = f"""
You are {personality}.

Your job is to completely behave like this character.
Never break character.
Respond exactly in the style, tone, personality and vocabulary of this character.

Rules:
- Stay in character.
- Never say you are an AI.
- Answer in a {response_length.lower()} way.
- Continue the conversation naturally.

Previous Conversation:

{conversation}
"""

    with st.spinner("Connecting to the Multiverse..."):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=ai_instruction
        )

    answer = response.text

    with st.chat_message("assistant"):
        st.markdown(answer)

    # Save AI Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# Download Chat
if st.session_state.messages:

    chat_text = ""

    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_text += f"User: {message['content']}\n"
        else:
            chat_text += f"AI: {message['content']}\n"

    st.download_button(
        "📥 Download Chat",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )