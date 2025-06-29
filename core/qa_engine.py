from transformers import pipeline
import re

qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def answer_question_with_justification(context, question):
    answer_data = qa_model(question=question, context=context)
    answer = answer_data["answer"]
    snippet = find_supporting_snippet(context, answer)
    return answer, snippet

def find_supporting_snippet(context, answer):
    match = re.search(rf"(.{{0,50}}{re.escape(answer)}.{{0,50}})", context)
    return match.group(0).strip() if match else "No clear supporting text found."
