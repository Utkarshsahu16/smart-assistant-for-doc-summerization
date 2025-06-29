from difflib import SequenceMatcher

def evaluate_answer(user_answer, correct_answer):
    ratio = SequenceMatcher(None, user_answer.lower(), correct_answer.lower()).ratio()
    return "✅ Correct" if ratio > 0.7 else f"❌ Incorrect (Expected: {correct_answer})"
