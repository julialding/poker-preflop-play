from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
from datetime import datetime
import json
import os

app = Flask(__name__)
# Generate a random secret key on startup - this doesn't need to be kept secret
# since we're just using it for an educational app with no sensitive data
app.secret_key = os.urandom(24)

# Load quiz data
with open('static/quiz_data.json') as f:
    quiz_data = json.load(f)

positions = ["Early Position", "Middle Position", "Late Position", "Small Blind", "Big Blind"]
hands = ["AA", "KK", "QQ", "AKs", "AQs", "AJs", "KQs", "JTs", "T9s", "98s"]

# Dictionary to store correct decisions for each hand+position combination
correct_decisions = {
    ("AA", "Early Position"): "Raise",
    ("AA", "Middle Position"): "Raise",
    # Add more combinations here
}

@app.route('/')
def index():
    # Record the time user enters the site
    session['start_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('home.html')

@app.route('/reset')
def reset():
    # Clear quiz history and redirect to first question
    if 'quiz_history' in session:
        session.pop('quiz_history')
    return redirect(url_for('play', quiz_id=1))

@app.route('/learn')
def learn():
    return render_template('learn_pos.html')

@app.route('/learn/<int:page_id>')
def learn_page(page_id):
    # Record when user accesses each learning page
    session.setdefault('learning_history', []).append({
        'page': page_id,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    if page_id == 2:
        return render_template('learn_page_2.html')
    elif page_id == 1:
        return render_template('learn.html')
    elif page_id == 3:
        return render_template('learn_page_3.html')
    elif page_id == 0:
        return render_template('learn_page_0.html')
    else:
        return render_template('learn_pos.html')

@app.route('/play/<int:quiz_id>')
def play(quiz_id):
    # Find the quiz data for this question
    quiz = next((q for q in quiz_data['quiz_pages'] if q['id'] == quiz_id), None)
    if not quiz:
        return redirect(url_for('results'))
    
    return render_template('play.html', quiz=quiz)

@app.route('/get-hand')
def get_hand():
    hand = random.choice(hands)
    position = random.choice(positions)
    
    # Store the current hand and position in session
    session['current_hand'] = hand
    session['current_position'] = position
    session.setdefault('history', [])  # Initialize history if it doesn't exist
    
    return jsonify({"hand": hand, "position": position})

@app.route('/submit-decision', methods=['POST'])
def submit_decision():
    data = request.get_json()
    decision = data.get('decision')
    amount = data.get('amount', 0)
    quiz_id = data.get('quiz_id')
    
    # Find the quiz data and check if answer is correct
    quiz = next((q for q in quiz_data['quiz_pages'] if q['id'] == quiz_id), None)
    is_correct = False
    if quiz:
        button_info = quiz['buttons'].get(decision.lower())
        if button_info:
            is_correct = button_info['correct'] and button_info['amount'] == amount
    
    # Store the decision in session history
    history = session.setdefault('quiz_history', [])
    history.append({
        'quiz_id': quiz_id,
        'decision': decision,
        'amount': amount,
        'is_correct': is_correct,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    session['quiz_history'] = history  # Explicitly update session
    
    feedback = quiz['feedback']['correct'] if is_correct else quiz['feedback']['incorrect']
    
    return jsonify({
        "status": "success",
        "is_correct": is_correct,
        "feedback": feedback,
        "next_quiz": quiz_id + 1 if quiz_id < len(quiz_data['quiz_pages']) else None
    })

@app.route('/results')
def show_results():
    history = session.get('quiz_history', [])
    
    # Count only the most recent answer for each question
    latest_answers = {}
    for entry in history:
        latest_answers[entry['quiz_id']] = entry['is_correct']
    
    total_questions = len(quiz_data['quiz_pages'])
    correct_answers = sum(1 for is_correct in latest_answers.values() if is_correct)
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    return render_template('results.html', 
                         history=history,
                         score=score,
                         total_questions=total_questions,
                         correct_answers=correct_answers)

if __name__ == '__main__':
    app.run(debug=True, port=5001)