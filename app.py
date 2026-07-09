import streamlit as st
import google.generativeai as genai

# ---------------- CONFIG ----------------
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="AI Learning Buddy", page_icon="🎓")
st.title("🎓 AI Learning Buddy")
st.write("Learn any topic with simple explanations, examples, quizzes, and feedback.")

# ---------------- INPUTS ----------------
topic = st.text_input("Enter a topic", placeholder="Example: DBMS")

activity = st.selectbox(
    "Choose an activity",
    [
        "Explain Concept",
        "Real-Life Example",
        "Generate Quiz",
        "Evaluate My Answer",
        "Full Learning Session"
    ]
)

question_input = ""
learner_answer = ""

if activity == "Evaluate My Answer":
    question_input = st.text_area("Enter the quiz question")
    learner_answer = st.text_area("Enter your answer")

# ---------------- PROMPT BUILDER ----------------
def build_prompt(topic, activity, question_input="", learner_answer=""):
    if activity == "Explain Concept":
        return f"""
You are a beginner-friendly AI tutor.
Explain the topic "{topic}" in simple language for a beginner.

Instructions:
- Start with a short definition.
- Break the explanation into simple points.
- Avoid difficult jargon.
- End with a short summary.
"""

    elif activity == "Real-Life Example":
        return f"""
You are an AI learning buddy.
Give one simple real-life example of "{topic}".
First explain the example, then connect it to the topic clearly.
"""

    elif activity == "Generate Quiz":
        return f"""
Create 5 quiz questions on "{topic}" for a beginner learner.
After each question, provide the correct answer.
Keep the language simple and clear.
"""

    elif activity == "Evaluate My Answer":
        return f"""
You are an AI tutor evaluating a learner's answer.

Topic: {topic}
Question: {question_input}
Learner's Answer: {learner_answer}

Do the following:
1. Say whether the answer is correct, partially correct, or incorrect.
2. Explain what is right.
3. Explain what is missing or wrong.
4. Give the correct answer in simple language.
5. End with one improvement tip.
"""

    elif activity == "Full Learning Session":
        return f"""
You are an AI Learning Buddy teaching the topic "{topic}" to a beginner.

Your session must follow this order:
1. Explain the topic in simple language.
2. Give one real-life example.
3. Ask 3 short quiz questions one by one.
4. For each question, also provide the correct answer and a short feedback note.
5. End with a short recap of the topic.

Keep the tone beginner-friendly, encouraging, and clear.
"""

# ---------------- GENERATE ----------------
if st.button("Generate"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    elif activity == "Evaluate My Answer" and (not question_input.strip() or not learner_answer.strip()):
        st.warning("Please enter both the question and your answer.")
    else:
        prompt = build_prompt(topic, activity, question_input, learner_answer)
        try:
            response = model.generate_content(prompt)
            st.subheader("AI Buddy Response")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
