# Smart Assistant for Research Summarization

## Overview
Smart Assistant for Research Summarization is an AI-powered Streamlit-based application designed to enhance your research workflow. Whether you're a student, academic, or professional, this tool helps you interact more deeply with documents by:

- Reading and understanding uploaded PDF or TXT files  
- Generating concise, high-quality summaries  
- Answering context-based questions from users  
- Creating logic-based questions to test comprehension  
- Justifying every answer with accurate document snippets  

This assistant transforms passive reading into an active learning experience.

## Features

- Ask Anything Mode  
  Ask any question related to the document, and receive contextual answers with citations.

- Challenge Me Mode  
  Get quizzed with 3 AI-generated logic-based questions and receive real-time evaluation of your responses.

- Snippet-based Justification  
  Each answer comes with a referenced snippet from the source document, boosting trust and interpretability.

- User-Friendly Interface  
  A simple, clean, and interactive UI powered by Streamlit — no technical expertise needed.

## Installation

Ensure you have Python installed, then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

This will start the app on your local browser.

## Project Structure

```
core/           # NLP pipelines: summarization, QA, question generation
utils/          # Evaluation logic and helper functions
app.py          # Main Streamlit application
requirements.txt
README.md
```

## AI Models Used

- Summarization: distilbart-cnn-12-6  
  A lightweight and fast transformer model fine-tuned for abstractive summarization.

- Question Answering: distilbert-base-uncased-distilled-squad  
  Efficient for answering fact-based questions by locating relevant text passages.

- Question Generation: GPT-2  
  Generates diverse and relevant logic-based questions to assess understanding.

## Ideal Use Cases

- Academic research summarization
- Rapid comprehension of lengthy documents
- Self-assessment through logic-based questioning
- Enhancing document-based learning with AI

## Feedback & Contributions

We welcome feedback, feature requests, and contributions! If you find this tool useful or want to improve it, feel free to fork the repository or open an issue.
