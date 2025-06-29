from transformers import pipeline
from core.qa_engine import answer_question_with_justification

generator = pipeline("text-generation", model="gpt2")

def generate_challenge_questions(context):
    prompt = f"Generate 3 logic-based questions based on this document:\n{context[:1000]}"
    generated = generator(prompt, max_new_tokens=100, num_return_sequences=1)[0]["generated_text"]
    raw_questions = generated.strip().split("\n")
    questions = []
    for q in raw_questions:
        if len(q.strip()) > 10:
            ans, ctx = answer_question_with_justification(context, q.strip())
            questions.append({"question": q.strip(), "answer": ans, "context": ctx})
    return questions[:3]
