from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('sign_language.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip().lower()
        conn = get_db()
        cursor = conn.cursor()

        # Handle "search <word>"
        if user_input.startswith("search "):
            word = user_input.split(" ", 1)[1]
            cursor.execute("SELECT * FROM signs WHERE name = ?", (word,))
            sign = cursor.fetchone()
            if sign:
                result = f"Sign for '{word}':\nDescription: {sign['description']}\nVideo: {sign['video']}"
            else:
                error = f"I don't know the sign for '{word}' yet."

        # Handle "learn alphabet"
        elif user_input == "learn alphabet":
            result = "Here's a video to learn the sign language alphabet: https://example.com/sign-language-alphabet"

        # Handle "practice signs"
        elif user_input == "practice signs":
            cursor.execute("SELECT name, description FROM signs ORDER BY RANDOM() LIMIT 3")
            practice_signs = cursor.fetchall()
            result = "Let's practice these signs:\n\n"
            for sign in practice_signs:
                result += f"• {sign['name']}: {sign['description']}\n"

        # Handle "quiz me"
        elif user_input == "quiz me":
            cursor.execute("SELECT name, description FROM signs ORDER BY RANDOM() LIMIT 1")
            sign = cursor.fetchone()
            if sign:
                result = f"What is the sign for '{sign['name']}'?\n\nHint: It involves {sign['description']}"
            else:
                error = "No signs available for quiz."

        # Handle "learn phrases"
        elif user_input == "learn phrases":
            phrases = [
                "Hello, how are you?",
                "Nice to meet you",
                "Have a good day",
                "Thank you very much"
            ]
            result = "Common phrases:\n\n"
            for phrase in phrases:
                result += f"• {phrase}\n"
            cursor.execute("SELECT name, description FROM signs WHERE name IN ('hello', 'thank', 'good', 'nice')")
            related_signs = cursor.fetchall()
            if related_signs:
                result += "\nRelated signs:\n"
                for sign in related_signs:
                    result += f"• {sign['name']}: {sign['description']}\n"

        # Handle "help"
        elif user_input == "help":
            result = """Available Commands:
• search <word>: Find a sign
• learn alphabet: Learn the alphabet
• practice signs: Practice random signs
• quiz me: Test your knowledge
• learn phrases: Learn common phrases
• help: Show this help message"""

        else:
            error = "Invalid command. Type 'help' for options."

        conn.close()

    return render_template("index.html", error=error, result=result)

if __name__ == "__main__":
    # Initialize database and create tables
    conn = get_db()
    cursor = conn.cursor()
    
    # Create the signs table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            video TEXT,
            description TEXT
        )
    ''')

    # Insert sample data if table is empty
    cursor.execute("SELECT COUNT(*) FROM signs")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ('hello', 'https://www.youtube.com/watch?v=OcKefCuXyXI', 'Wave your hand with your palm facing outward'),
            ('goodbye', 'https://example.com/goodbye-sign', 'Wave your hand with your palm facing inward'),
            ('thank you', 'https://example.com/thank-you-sign', 'Make a flat "O" shape with your hand and move it away from your body'),
            ('yes', 'https://example.com/yes-sign', 'Nod your head up and down'),
            ('no', 'https://example.com/no-sign', 'Shake your head from side to side')
        ]
        cursor.executemany("INSERT OR IGNORE INTO signs (name, video, description) VALUES (?, ?, ?)", sample_data)
        conn.commit()
    
    conn.close()
    app.run(debug=True, port=5002)
