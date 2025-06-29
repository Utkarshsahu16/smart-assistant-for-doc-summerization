from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def generate_summary(text):
    # Break long text into chunks of 1000 characters
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = ""
    for chunk in chunks[:3]:  # Limit to 3 chunks (~150 words total)
        result = summarizer(chunk, max_length=80, min_length=30, do_sample=False)[0]["summary_text"]
        summary += result.strip() + " "
    return summary.strip()
