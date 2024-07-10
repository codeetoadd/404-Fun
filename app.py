from flask import Flask, render_template, send_from_directory
import os
import random  # Import the random module
import csv

app = Flask(__name__)

# Read CSV files only once when the application starts
dad_jokes = []
geeky_facts = []
short_poems = []

with open(os.path.join('static', 'DadJokes.csv'), newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dad_jokes.append(row['joke'])

with open(os.path.join('static', 'GeekyFacts.csv'), newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        geeky_facts.append(row['Fact'])

with open(os.path.join('static', 'ShortPoems.csv'), newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        short_poems.append(row['Poem'])

# Global index to track the current position in the sequence
current_index = 0
sequence = ['fact', 'joke', 'poem']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/random-text')
def random_text():
    global current_index

    text_type = sequence[current_index]

    if text_type == 'joke':
        text_content = random.choice(dad_jokes)
    elif text_type == 'fact':
        text_content = random.choice(geeky_facts)
    else:
        text_content = random.choice(short_poems)

    # Update the index to point to the next item in the sequence
    current_index = (current_index + 1) % len(sequence)

    return text_content

if __name__ == '__main__':
    app.run(debug=True)
