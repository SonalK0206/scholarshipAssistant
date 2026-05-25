import streamlit as st
from groq import Groq

# 1. Page Configuration and UI Setup
st.set_page_config(page_title="Scholarship Finder AI", page_icon="🎓", layout="wide")
st.title("ScholarAssist: AI Scholarship Matchmaker")
st.write("Find financial aid, fellowships, and grants tailored to your educational class, field of study, geographical region, income bracket, and gender.")

# The app automatically grabs the API key from your secure cloud settings internally
api_key_to_use = st.secrets.get("GROQ_API_KEY", "")

# Sidebar setup with no API key inputs
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
    
    # Internal validation to ensure your cloud dashboard has the key configured
    if not api_key_to_use:
        st.error("System configuration error: Groq API key missing in cloud secrets.")
        st.stop()

    client = Groq(api_key=api_key_to_use)

    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    with st.chat_message("assistant"):
        try:
            # --- STEP A: DEEP CONTEXT-AWARE INTENT CLASSIFICATION ---
            intent_check = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an advanced educational routing agent. Determine if the user's input is a valid "
                            "academic or geographical context query meant for locating student aid.\n\n"
                            "Reply with exactly one word: 'VALID' or 'IRRELEVANT'.\n\n"
                            "Classify as 'VALID' if the user mentions ANY of the following:\n"
                            "- Educational levels/classes: school standards (class 10, 11th, 12th, metric), degrees (B.Tech, B.Sc, MBBS, UG, PG), or phrases like 'studying in school'.\n"
                            "- Fields of study or specific educational streams: engineering, arts, commerce, sciences, etc.\n"
                            "- Geographical locations/places: countries (India, USA), states (Karnataka, Maharashtra), cities (Mumbai, Bangalore), or phrases indicating local regions.\n"
                            "- Demographic traits: income levels, categories, or gender markers.\n"
                            "- Conversational baseline inputs: simple greetings like 'hi', 'hello', or 'good morning'.\n\n"
                            "Classify as 'IRRELEVANT' ONLY if the input is completely detached from a student or academic financial context, "
                            "such as holiday planning/traveling, cooking, standard programming help, video games, or entertainment."
                        )
                    },
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0
            )
            
            user_intent = intent_check.choices[0].message.content.strip().upper()

            # --- STEP B: ROUTING LOGIC ---
            if "IRRELEVANT" in user_intent:
                ai_reply = "Please ask questions related only to school/college standards, locations, scholarships, grants, and academic financial assistance. I am here to support your educational funding journey!"
                st.write(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
            else:
                scholarship_bot_messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are an expert Academic Financial Consultant and Scholarship Matchmaker. "
                            "Your goal is to help students find relevant scholarships, grants, and fellowships based on "
                            "their current class/standard, field of study, region, annual family income, and gender.\n\n"
                            "Strict Response Formatting Rules:\n"
                            "1. Actively cross-reference matching criteria based on the user's educational class (school vs college levels) and location.\n"
                            "2. For EACH scholarship listed, you must provide using standard markdown bold text:\n"
                            "   - Name of the Scholarship\n"
                            "   - Eligibility Criteria (Explicitly highlight required class, region, income cap, and gender parameters)\n"
                            "   - Financial Reward/Benefit\n"
                            "   - Typical Application Timeline/Deadlines\n"
                            "3. DO NOT use any graphic icons or raw emoji symbols in your text response to prevent layout compilation errors.\n"
                            "4. If the input is just a greeting (like 'hi' or 'hello'), reply with a friendly welcome "
                            "   and remind them to share their current class, region, income, and gender.\n"
                            "5. Maintain an encouraging, helpful, and highly professional tone."
                        )
                    }
                ]

                # Append past conversation history for continuous context
                for msg in st.session_state.messages:
                    scholarship_bot_messages.append({"role": msg["role"], "content": msg["content"]})

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=scholarship_bot_messages,
                    temperature=0.4
                )
                
                ai_reply = response.choices[0].message.content
                st.write(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
        except Exception as e:
            st.error(f"System Error: {str(e)}")
