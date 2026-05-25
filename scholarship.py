import streamlit as st
from groq import Groq

# 1. Page Configuration and UI Setup
st.set_page_config(page_title="Scholarship Finder AI", page_icon="degree", layout="wide")
st.title("ScholarAssist: AI Scholarship Matchmaker")
st.write("Find financial aid, fellowships, and grants tailored to your educational class, field of study, geographical region, income bracket, and gender.")

# Try to fetch the secret key from the cloud environment first
secret_key = st.secrets.get("GROQ_API_KEY", "")

# Sidebar input can now be left completely optional/blank for users
groq_key_input = st.sidebar.text_input("Enter Groq API Key (Optional)", type="password", value=secret_key)

st.sidebar.markdown("---")
st.sidebar.subheader("Tips for Best Results")
st.sidebar.write("Provide details such as your Current Class/Standard, Field of Study, State/Region, Annual Family Income, and Gender to unlock specialized matching schemes.")

# 2. Maintain Chat Memory
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant", 
            "content": "Hello! I am your AI Scholarship Assistant. Please tell me your current educational class (e.g., Class 10, 12th, B.Tech), the region or state you belong to, your annual family income bracket, and gender. I will find matching financial aid options for you!"
        }
    ]

# Display previous chat texts
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 3. Handle User Input and Groq API Execution
if user_prompt := st.chat_input("e.g., I am in class 12 in Maharashtra, family income is 1.5 Lakhs. Any scholarships?"):
    # Use the sidebar input if provided, otherwise fall back to your secure cloud secret key
    api_key_to_use = groq_key_input if groq_key_input else secret_key

    if not api_key_to_use:
        st.info("System configuration error: Groq API key missing.")
        st.stop()

    client = Groq(api_key=api_key_to_use)

    # ... [The rest of your existing message handling and try/except code stays exactly the same]
