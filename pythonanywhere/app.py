from flask import Flask, render_template, send_from_directory
import os
import random
import csv

app = Flask(__name__)

# Function to read CSV files
def read_csv_file(file_path, field_name):
    data = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row[field_name])
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error reading file '{file_path}': {str(e)}")
    return data

# Define absolute file paths
dad_jokes_path = '/home/404web/mysite/DadJokes.csv'
geeky_facts_path = '/home/404web/mysite/GeekyFacts.csv'
short_poems_path = '/home/404web/mysite/ShortPoems.csv'

# Read CSV files only once when the application starts
dad_jokes = read_csv_file(dad_jokes_path, 'joke')
geeky_facts = read_csv_file(geeky_facts_path, 'Fact')
short_poems = read_csv_file(short_poems_path, 'Poem')

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
        if dad_jokes:
            text_content = random.choice(dad_jokes)
        else:
            text_content = "No jokes available."
    elif text_type == 'fact':
        if geeky_facts:
            text_content = random.choice(geeky_facts)
        else:
            text_content = "No geeky facts available."
    else:
        if short_poems:
            text_content = random.choice(short_poems)
        else:
            text_content = "No poems available."

    # Update the index to point to the next item in the sequence
    current_index = (current_index + 1) % len(sequence)

    return text_content

if __name__ == '__main__':
    app.run(debug=True)
