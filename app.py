from flask import Flask, render_template, request, jsonify
import sqlite3
import random

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('sign_language.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database with sample signs
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create the signs table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signs (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            description TEXT,
            video TEXT
        )
    ''')
    
    # Sample data
    sample_signs = [
        ('hello', 'Wave your hand with your palm facing outward', 'https://example.com/hello'),
        ('goodbye', 'Wave your hand with your palm facing inward', 'https://example.com/goodbye'),
        ('thank you', 'Touch your chin with your fingertips and move your hand forward', 'https://example.com/thankyou'),
        ('please', 'Rub your chest in a circular motion', 'https://example.com/please'),
        ('sorry', 'Make a fist and rub it in a circular motion over your chest', 'https://example.com/sorry'),
        ('yes', 'Make your hand into a fist and nod it up and down', 'https://example.com/yes'),
        ('no', 'Extend your index and middle fingers and move them back and forth', 'https://example.com/no'),
        ('help', 'Make a thumbs up with one hand and move it up the palm of your other hand', 'https://example.com/help'),
        ('love', 'Cross your arms over your chest', 'https://example.com/love'),
        ('friend', 'Hook your index fingers together', 'https://example.com/friend')
    ]
    
    # Insert sample data
    for sign in sample_signs:
        try:
            cursor.execute("INSERT OR IGNORE INTO signs (name, description, video) VALUES (?, ?, ?)", sign)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()

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
                result = f"Sign for '{word}':\nDescription: {sign['description']}"
            else:
                error = f"I don't know the sign for '{word}' yet."

        # Handle "learn alphabet"
        elif user_input == "learn alphabet":
            result = "Here's how to sign the alphabet: [Video demonstration coming soon]"

        # Handle "practice signs"
        elif user_input == "practice signs":
            cursor.execute("SELECT name, description FROM signs ORDER BY RANDOM() LIMIT 3")
            signs = cursor.fetchall()
            result = "Let's practice these signs:\n\n"
            for sign in signs:
                result += f"• {sign['name'].capitalize()}: {sign['description']}\n"

        # Handle "learn phrases"
        elif user_input == "learn phrases":
            result = """Common phrases in sign language:
• "Hello, how are you?"
• "Nice to meet you"
• "Thank you very much"
• "Please and thank you"
• "Have a good day"
"""

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

@app.route("/quiz", methods=["GET"])
def quiz():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get all signs for multiple choice options
        cursor.execute("SELECT name, description FROM signs")
        all_signs = cursor.fetchall()
        
        if not all_signs:
            return jsonify({"error": "No signs available for quiz."})
        
        # Select random sign for question
        correct_sign = random.choice(all_signs)
        
        # Get 3 random incorrect options
        other_signs = [sign for sign in all_signs if sign['name'] != correct_sign['name']]
        wrong_options = random.sample(other_signs, min(3, len(other_signs)))
        
        # Create options list with correct and incorrect answers
        options = [correct_sign['name']] + [sign['name'] for sign in wrong_options]
        random.shuffle(options)
        
        return jsonify({
            "question": f"What sign matches this description?\n\n{correct_sign['description']}",
            "options": options,
            "answer": correct_sign['name']
        })
        
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()  # Initialize database with sample signs
    app.run(debug=True, port=5002)
