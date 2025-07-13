from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from core.file_processor import extract_text_from_file
from core.summarizer import generate_summary
from core.qa_engine import answer_question_with_justification
from core.question_gen import generate_challenge_questions
from utils.helpers import evaluate_answer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store document text in memory (in production, use a proper database)
document_text = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Create a file-like object for the processor
            class FileWrapper:
                def __init__(self, filepath):
                    self.filepath = filepath
                    self.type = "application/pdf" if filename.endswith('.pdf') else "text/plain"
                
                def read(self):
                    with open(self.filepath, 'rb') as f:
                        return f.read()
            
            file_obj = FileWrapper(filepath)
            text = extract_text_from_file(file_obj)
            
            # Store text with a session ID (in production, use proper session management)
            session_id = request.form.get('session_id', 'default')
            document_text[session_id] = text
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({'success': True, 'message': 'File processed successfully'})
        
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    
    if session_id not in document_text:
        return jsonify({'error': 'No document loaded'}), 400
    
    try:
        summary = generate_summary(document_text[session_id])
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    question = data.get('question')
    
    if session_id not in document_text:
        return jsonify({'error': 'No document loaded'}), 400
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        answer, snippet = answer_question_with_justification(document_text[session_id], question)
        return jsonify({'answer': answer, 'snippet': snippet})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/challenge', methods=['POST'])
def get_challenge_questions():
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    
    if session_id not in document_text:
        return jsonify({'error': 'No document loaded'}), 400
    
    try:
        questions = generate_challenge_questions(document_text[session_id])
        return jsonify({'questions': questions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate_answer():
    data = request.get_json()
    user_answer = data.get('user_answer')
    correct_answer = data.get('correct_answer')
    context = data.get('context')
    
    if not all([user_answer, correct_answer]):
        return jsonify({'error': 'Missing answer data'}), 400
    
    try:
        score = evaluate_answer(user_answer, correct_answer)
        return jsonify({'score': score, 'context': context})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
