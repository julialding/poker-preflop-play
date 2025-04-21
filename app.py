from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

positions = ["Early Position", "Middle Position", "Late Position", "Small Blind", "Big Blind"]
hands = ["AA", "KK", "QQ", "AKs", "AQs", "AJs", "KQs", "JTs", "T9s", "98s"]

@app.route('/')
def index():
    return render_template('learn.html')

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/get-hand')
def get_hand():
    hand = random.choice(hands)
    position = random.choice(positions)
    return jsonify({"hand": hand, "position": position})

if __name__ == '__main__':
   app.run(debug = True, port=5001)
