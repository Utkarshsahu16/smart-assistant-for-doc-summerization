// Dark mode toggle
const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    localStorage.setItem('darkMode', document.body.classList.contains('dark'));
    darkModeToggle.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
});
// Restore dark mode
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark');
    darkModeToggle.textContent = '☀️';
}

const fileInput = document.getElementById('fileInput');
const uploadStatus = document.getElementById('uploadStatus');
const summarySection = document.getElementById('summarySection');
const summaryContent = document.getElementById('summaryContent');
const modeSection = document.getElementById('modeSection');
const modeSelect = document.getElementById('modeSelect');
const askSection = document.getElementById('askSection');
const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');
const answerContent = document.getElementById('answerContent');
const challengeSection = document.getElementById('challengeSection');
const challengeQuestions = document.getElementById('challengeQuestions');

// Simple session id for demo
const sessionId = 'default';

fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    uploadStatus.textContent = 'Uploading...';
    summarySection.classList.add('hidden');
    modeSection.classList.add('hidden');
    askSection.classList.add('hidden');
    challengeSection.classList.add('hidden');
    answerContent.textContent = '';
    challengeQuestions.innerHTML = '';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', sessionId);

    try {
        const res = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (data.success) {
            uploadStatus.textContent = 'File uploaded! Generating summary...';
            await getSummary();
        } else {
            uploadStatus.textContent = data.error || 'Upload failed.';
        }
    } catch (err) {
        uploadStatus.textContent = 'Error uploading file.';
    }
});

async function getSummary() {
    try {
        const res = await fetch('/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId })
        });
        const data = await res.json();
        if (data.summary) {
            summaryContent.textContent = data.summary;
            summarySection.classList.remove('hidden');
            modeSection.classList.remove('hidden');
        } else {
            summaryContent.textContent = data.error || 'Could not generate summary.';
            summarySection.classList.remove('hidden');
        }
    } catch (err) {
        summaryContent.textContent = 'Error generating summary.';
        summarySection.classList.remove('hidden');
    }
}

modeSelect.addEventListener('change', () => {
    updateMode();
});

function updateMode() {
    askSection.classList.add('hidden');
    challengeSection.classList.add('hidden');
    answerContent.textContent = '';
    challengeQuestions.innerHTML = '';
    if (modeSelect.value === 'ask') {
        askSection.classList.remove('hidden');
    } else if (modeSelect.value === 'challenge') {
        getChallengeQuestions();
    }
}

askBtn.addEventListener('click', async () => {
    const question = questionInput.value.trim();
    if (!question) return;
    answerContent.textContent = 'Thinking...';
    try {
        const res = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, question })
        });
        const data = await res.json();
        if (data.answer) {
            answerContent.innerHTML = `<b>Answer:</b> ${data.answer}<br><span class='caption'>📚 Justification: ${data.snippet}</span>`;
        } else {
            answerContent.textContent = data.error || 'Could not get answer.';
        }
    } catch (err) {
        answerContent.textContent = 'Error getting answer.';
    }
});

async function getChallengeQuestions() {
    challengeQuestions.innerHTML = 'Loading questions...';
    try {
        const res = await fetch('/challenge', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId })
        });
        const data = await res.json();
        if (data.questions) {
            challengeQuestions.innerHTML = '';
            data.questions.forEach((q, i) => {
                const qDiv = document.createElement('div');
                qDiv.className = 'challenge-q';
                qDiv.innerHTML = `
                    <div><b>Q${i+1}:</b> ${q.question}</div>
                    <input type="text" id="userAnswer${i}" placeholder="Your answer...">
                    <button onclick="submitChallengeAnswer(${i}, '${encodeURIComponent(q.answer)}', '${encodeURIComponent(q.context)}')">Submit</button>
                    <div id="eval${i}"></div>
                `;
                challengeQuestions.appendChild(qDiv);
            });
            challengeSection.classList.remove('hidden');
        } else {
            challengeQuestions.textContent = data.error || 'Could not get questions.';
            challengeSection.classList.remove('hidden');
        }
    } catch (err) {
        challengeQuestions.textContent = 'Error getting questions.';
        challengeSection.classList.remove('hidden');
    }
}

window.submitChallengeAnswer = async function(idx, answer, context) {
    const userInput = document.getElementById(`userAnswer${idx}`);
    const evalDiv = document.getElementById(`eval${idx}`);
    const user_answer = userInput.value.trim();
    if (!user_answer) return;
    evalDiv.textContent = 'Evaluating...';
    try {
        const res = await fetch('/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_answer,
                correct_answer: decodeURIComponent(answer),
                context: decodeURIComponent(context)
            })
        });
        const data = await res.json();
        if (data.score) {
            evalDiv.innerHTML = `<b>Evaluation:</b> ${data.score}<br><span class='caption'>📚 Justification: ${data.context}</span>`;
        } else {
            evalDiv.textContent = data.error || 'Could not evaluate.';
        }
    } catch (err) {
        evalDiv.textContent = 'Error evaluating.';
    }
}

// Show ask/challenge section on mode change after summary
document.addEventListener('DOMContentLoaded', () => {
    updateMode();
}); 