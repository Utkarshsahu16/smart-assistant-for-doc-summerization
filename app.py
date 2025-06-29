import streamlit as st
from core.file_processor import extract_text_from_file
from core.summarizer import generate_summary
from core.qa_engine import answer_question_with_justification
from core.question_gen import generate_challenge_questions
from utils.helpers import evaluate_answer

st.set_page_config(page_title="Smart Research Assistant", layout="wide")
st.title("📄 Smart Assistant for Research Summarization")

uploaded_file = st.file_uploader("Upload PDF or TXT document", type=["pdf", "txt"])

if uploaded_file:
    doc_text = extract_text_from_file(uploaded_file)

    st.subheader("🔍 Auto Summary")
    with st.spinner("Generating summary..."):
        summary = generate_summary(doc_text)
        st.write(summary)

    mode = st.radio("Choose Mode", ["Ask Anything", "Challenge Me"])

    if mode == "Ask Anything":
        question = st.text_input("Ask a question:")
        if question:
            with st.spinner("Thinking..."):
                answer, snippet = answer_question_with_justification(doc_text, question)
                st.markdown(f"**Answer:** {answer}")
                st.caption(f"📚 Justification: {snippet}")

    elif mode == "Challenge Me":
        questions = generate_challenge_questions(doc_text)
        for i, q in enumerate(questions, 1):
            user_answer = st.text_input(f"Q{i}: {q['question']}", key=f"q{i}")
            if user_answer:
                score = evaluate_answer(user_answer, q['answer'])
                st.markdown(f"**Evaluation:** {score}")
                st.caption(f"📚 Justification: {q['context']}")
