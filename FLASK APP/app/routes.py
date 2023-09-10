# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

bp = Blueprint('main', __name__)



# Define the quiz data as mentioned in Step 1
quiz_data = [
    {
        'question': 'Question 1?',
        'options': ['Option A', 'Option B', 'Option C', 'Option D'],
        'correct_answer': 'Option A',
    },
    {
        'question': 'Question 2?',
        'options': ['Option A', 'Option B', 'Option C', 'Option D'],
        'correct_answer': 'Option B',
    },{
        'question': 'Question 3?',
        'options': ['Option A', 'Option B', 'Option C', 'Option D'],
        'correct_answer': 'Option C',
    },
    # Add more questions here...
]

# Define the correct answers for each question (assuming the same order as quiz_data)
correct_answers = [question['correct_answer'] for question in quiz_data]

@bp.route('/')
def home():
    return render_template('home.html')



@bp.route('/camera')
def camera():
    return render_template('camera.html')

@bp.route('/carbon_footprint')
def carbon_footprint():
    return render_template('carbon_footprint.html')

@bp.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')    

@bp.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        session['score'] = 0  # Initialize the score
        session['question_number'] = 0  # Initialize the question number
        return redirect(url_for('main.quiz_question', question_number=0))

    return render_template('quiz.html')

@bp.route('/quiz/question/<int:question_number>', methods=['GET', 'POST'])
def quiz_question(question_number):
    if 'score' not in session:
        return redirect(url_for('main.quiz'))

    if question_number >= len(quiz_data):
        return redirect(url_for('main.quiz_result'))

    question_info = quiz_data[question_number]
    question = question_info['question']
    options = question_info['options']

    if request.method == 'POST':
        selected_option = request.form.get('answer')
        correct_answer = question_info['correct_answer']

        if selected_option == correct_answer:
            session['score'] += 1

        action = request.form.get('action')

        if action == 'next':
            session['question_number'] += 1
            return redirect(url_for('main.quiz_question', question_number=question_number + 1))

    return render_template('question.html', question_number=question_number, question=question, options=options)

@bp.route('/quiz/result', methods=['GET'])
def quiz_result():
    if 'score' not in session:
        return redirect(url_for('main.quiz'))

    score = session['score']
    session.pop('score', None)
    session.pop('question_number', None)
    return render_template('result.html', score=score)

@bp.route('/show_correct_answers', methods=['POST'])
def show_correct_answers():
    # Enumerate the quiz data along with indices
    enumerated_quiz_data = list(enumerate(quiz_data, start=1))

    return render_template('correct_answers.html', enumerated_quiz_data=enumerated_quiz_data, correct_answers=correct_answers)

@bp.route('/play_again', methods=['POST'])
def play_again():
    session.pop('score', None)
    session.pop('question_number', None)
    return redirect(url_for('main.home'))

