from flask import Flask, render_template, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# Connect to SQLite database. It will be created if it doesn't exist.
conn = sqlite3.connect('sign_language.db', check_same_thread=False)
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS signs
             (word text PRIMARY KEY, description text, ascii text)''')
conn.commit()

# Pre-populate the database with some words
default_signs = [
    ("hello", "A friendly greeting", """
        ____
       /    \\
      |  o  o |
       \\____/
    """),
    ("goodbye", "A farewell gesture", """
        ____
       /    \\
      |  ^  ^ |
       \\______/
    """),
    ("thank you", "An expression of gratitude", """
        ____
       /    \\
      |  -  - |
       \\______/
    """),
    ("yes", "An affirmative response", """
        ____
       /    \\
      |  >  < |
       \\______/
    """),
    ("no", "A negative response", """
        ____
       /    \\
      |  x  x |
       \\______/
    """),
    ("please", "A polite request", """
        ____
       /    \\
      |  ~  ~ |
       \\______/
    """),
    ("sorry", "An expression of apology", """
        ____
       /    \\
      |  T  T |
       \\______/
    """),
    ("help", "Request for assistance", """
        ____
       /    \\
      |  ?  ? |
       \\______/
    """),
    ("love", "An expression of affection", """
        ____
       /    \\
      |  <3 <3 |
       \\______/
    """),
    ("friend", "A person you know and like", """
        ____
       /    \\
      |  U  U |
       \\______/
    """)
]

# Insert default signs into the database
for word, description, ascii_art in default_signs:
    try:
        c.execute("INSERT INTO signs VALUES (?, ?, ?)", (word, description, ascii_art))
    except sqlite3.IntegrityError:
        pass  # Skip if the word already exists
conn.commit()
conn.close()

# Function to get all signs from the database
def get_signs():
    conn = sqlite3.connect('sign_language.db')
    c = conn.cursor()
    c.execute("SELECT * FROM signs")
    rows = c.fetchall()
    conn.close()
    return rows

# Function to add a new sign to the database
def add_sign(word, description, ascii):
    conn = sqlite3.connect('sign_language.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO signs VALUES (?, ?, ?)", (word, description, ascii))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Word already exists
    finally:
        conn.close()
    return True

# Function to get a sign by word from the database
def get_sign_by_word(word):
    conn = sqlite3.connect('sign_language.db')
    c = conn.cursor()
    c.execute("SELECT * FROM signs WHERE word=?", (word,))
    row = c.fetchone()
    conn.close()
    return row

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip().lower()

        # Handle "hello"
        if user_input == "hello":
            result = "Hello! How can I help you today? Type 'help' for a list of commands."

        # Handle "search <word>"
        elif user_input.startswith("search "):
            word = user_input.split(" ", 1)[1]
            row = get_sign_by_word(word)
            if row:
                result = f"<strong>{row[0].capitalize()}:</strong><br>{row[1]}<br><pre>{row[2]}</pre>"
            else:
                error = f"I don't know the sign for '{word}' yet."

        # Handle "learn <word>"
        elif user_input.startswith("learn "):
            word = user_input.split(" ", 1)[1]
            row = get_sign_by_word(word)
            if row:
                result = f"<strong>Teaching:</strong> {row[0].capitalize()}<br>{row[1]}<br><pre>{row[2]}</pre>"
            else:
                error = f"I don't know '{word}' yet. Use 'teach {word} <description>' to add it."

        # Handle "teach <word> <description>"
        elif user_input.startswith("teach ") and len(user_input.split()) >= 3:
            parts = user_input.split(" ", 2)  # Split into ["teach", "<word>", "<description>"]
            word_to_teach = parts[1]
            description = parts[2]
            ascii_art = """
                              _______
                             /       \\
                            |   o   o |
                             _______/"""
            if add_sign(word_to_teach, description, ascii_art):
                result = f"Thanks! I've learned the sign for '{word_to_teach}'."
            else:
                error = f"The word '{word_to_teach}' already exists in the database."

        # Handle "list"
        elif user_input == "list":
            rows = get_signs()
            if rows:
                result = "<strong>Words I know:</strong><br>" + "<br>".join([row[0] for row in rows])
            else:
                error = "No signs available in the database."

        # Handle "help"
        elif user_input == "help":
            result = """
            <strong>Available Commands:</strong><br>
            - <code>hello</code>: Greet the bot.<br>
            - <code>search &lt;word&gt;</code>: Search for a sign.<br>
            - <code>learn &lt;word&gt;</code>: Learn a sign.<br>
            - <code>teach &lt;word&gt; &lt;description&gt;</code>: Teach a new sign.<br>
            - <code>list</code>: List all words I know.<br>
            - <code>quiz</code>: Take a quiz on signs.<br>
            - <code>help</code>: Show this help message.
            """

        # Handle "quiz"
        elif user_input == "quiz":
            rows = get_signs()
            if rows:
                selected_row = random.choice(rows)
                result = f"<strong>Quiz:</strong> What is the sign for '{selected_row[0]}'?"
            else:
                error = "No signs available."

        # Handle invalid commands
        else:
            error = "Invalid command. Type 'help' for options."

    return render_template("index.html", error=error, result=result)

@app.route("/quiz", methods=["GET"])
def quiz():
    signs = get_signs()
    if not signs:
        return jsonify({"error": "No signs available in the database."})

    # Randomly select a sign for the quiz
    selected_sign = random.choice(signs)
    word = selected_sign[0]
    description = selected_sign[1]

    # Return a JSON response with the question, hint, and answer
    return jsonify({
        "question": f"What is the sign for '{word}'?",
        "hint": description,
        "answer": word
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
