from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

positions = ["Early Position", "Middle Position", "Late Position", "Small Blind", "Big Blind"]
hands = ["AA", "KK", "QQ", "AKs", "AQs", "AJs", "KQs", "JTs", "T9s", "98s"]

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/learn/<int:page_id>')
def learn_page(page_id):
    if page_id == 2:
        return render_template('learn_page_2.html')
    elif page_id == 3:
        return render_template('learn_page_3.html')
    else:
        return render_template('learn.html')

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/get-hand')
def get_hand():
    hand = random.choice(hands)
    position = random.choice(positions)
    return jsonify({"hand": hand, "position": position})

@app.route('/results')
def show_results():
    pass

if __name__ == '__main__':
   app.run(debug=True, port=5001)