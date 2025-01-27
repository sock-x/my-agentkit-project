from flask import Flask, render_template, request
import random

app = Flask(__name__)

signs = {
    "hello": {
        "description": "Wave your hand.",
        "ascii": """
  ___
 /   \\
|     |
 \\___/
"""
    },
    "thank you": {
        "description": "Place your hand near your chin and move it forward.",
        "ascii": """
  ___
 /   \\
|     |
 \\___/
"""
    },
    "goodbye": {
        "description": "Wave your hand like you're saying goodbye.",
        "ascii": """
  ___
 /   \\
|     |
 \\___/
"""
    },
}

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip().lower()

        # Handle "search <word>"
        if user_input.startswith("search "):
            word = user_input.split(" ", 1)[1]
            if word in signs:
                data = signs[word]
                result = f"{data['description']}\n\n{data['ascii']}"
            else:
                error = f"I don't know the sign for '{word}' yet."

        # Handle "learn <word>"
        elif user_input.startswith("learn "):
            word = user_input.split(" ", 1)[1]
            if word in signs:
                data = signs[word]
                result = f"Teaching: {word}\n{data['description']}\n{data['ascii']}"
            else:
                error = f"I don't know '{word}' yet. Use 'teach {word} <description>' to add it."

        # Handle "teach <word> <description>"
        elif user_input.startswith("teach "):
            parts = user_input.split(" ", 2)  # Split into ["teach", "word", "description"]
            if len(parts) >= 3:
                word = parts[1]
                description = parts[2]
                signs[word] = {
                    "description": description,
                    "ascii": "ASCII_GOES_HERE"  # Add your ASCII art logic
                }
                result = f"Thanks! I've learned the sign for '{word}'."
            else:
                error = "Invalid format. Use: teach <word> <description>"

        # Handle "quiz" command
        elif user_input == "quiz":
            word = random.choice(list(signs.keys()))
            result = f"Quiz: What's the sign for '{word}'?"

        # Handle "help"
        elif user_input == "help":
            result = """
            Available Commands:
            - search <word>: Find a sign
            - learn <word>: Learn a sign
            - teach <word> <description>: Add a new sign
            - quiz: Start a quiz
            """

        else:
            error = "Invalid command. Type 'help' for options."

    return render_template("index.html", error=error, result=result)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
