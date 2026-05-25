import streamlit as st
import requests
from groq import Groq

# 1. Page Configuration and UI Setup
st.set_page_config(page_title="Free AI Travel Guide", page_icon="✈️")
st.title("🗺️ Free AI Personal Travel Assistant")
st.write("Enter a city or country, and Meta's Llama 3.3 will build your itinerary for free!")

# Secure sidebar input for your Free Groq API Key
groq_key_input = st.sidebar.text_input("Enter Groq API Key", type="password")

# 2. Function to fetch live helper context (Wikipedia API - 100% Free)
def fetch_location_context(location):
    url = f"https://wikipedia.org{location.replace(' ', '_')}"
    headers = {'User-Agent': 'TravelBot/1.0'}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json().get('extract', '')
    except:
        return ""
    return ""

# 3. Maintain Conversational Memory
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! What city or country are you traveling to?"}]

# Display previous chat texts
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 4. Handle User Input and Groq API Execution
if user_prompt := st.chat_input():
    if not groq_key_input:
        st.info("Please enter your free Groq API key in the sidebar to start.")
        st.stop()

    # Initialize the official Groq client
    client = Groq(api_key=groq_key_input)

    # Show user message immediately on screen
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    # Fetch live factual data about the destination
    wiki_context = fetch_location_context(user_prompt)

    # Build structured prompts for the open-source model
    groq_messages = [
        {
            "role": "system",
            "content": (
                "You are an elite AI Travel Guide. Recommend the best spots to visit based on the location provided. "
                "Structure your response beautifully using emojis: 🏛️ Top Landmarks, 🍔 Food Spots, and 🌲 Hidden Gems. "
                "Keep descriptions short, conversational, and highly engaging."
            )
        },
        {
            "role": "system", 
            "content": f"Factual background context for accuracy: {wiki_context}"
        }
    ]

    # Append past conversation history so it remembers previous context
    for msg in st.session_state.messages:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})

    # Call the Free Groq Chat Engine
    with st.chat_message("assistant"):
        try:
            # Utilizing 'llama-3.3-70b-versatile', the absolute best free production model
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=groq_messages,
                temperature=0.7
            )
            
            ai_reply = response.choices[0].message.content
            st.write(ai_reply)
            
            # Save response to history array
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
        except Exception as e:
            st.error(f"Groq API Error: {str(e)}")
