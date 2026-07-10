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

if "history" not in st.session_state:
    st.session_state.history = []

user_message = st.text_input("Say something:")

col1, col2 = st.columns(2)

with col1:
    send = st.button("🚀 SEND")

with col2:
    clear = st.button("🗑 CLEAR CHAT")

if clear:
    st.session_state.history = []
    st.rerun()

if send:

    if user_message:

        persona = personality

        conversation = ""

        for chat in st.session_state.history:
            conversation += f"User: {chat['user']}\n"
            conversation += f"AI: {chat['ai']}\n"

        ai_instruction = f"""
You are {persona}.

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

User:
{user_message}
"""

        with st.spinner("Connecting to the Multiverse..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=ai_instruction
            )

        answer = response.text

        st.session_state.history.append(
            {
                "user": user_message,
                "ai": answer
            }
        )

        st.success("Message received!")

    else:
        st.warning("Please type a message first.")

if st.session_state.history:

    st.subheader("💬")

    for chat in st.session_state.history:

        st.markdown(f"**🧑 You:** {chat['user']}")
        st.markdown(f"**🤖 {personality}:** {chat['ai']}")
        st.divider()

    chat_text = ""

    for chat in st.session_state.history:
        chat_text += f"User: {chat['user']}\n"
        chat_text += f"AI: {chat['ai']}\n\n"

    st.download_button(
        "📥 Download Chat",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )