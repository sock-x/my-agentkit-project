from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Dictionary to store signs with descriptions and ASCII art
signs = {
    "alphabet": {
        "A": {
            "description": "Make a fist with your thumb on the side.",
            "ascii": """
  ____
 /    \\
|      |
 \\____/
"""
        },
        "B": {
            "description": "Hold your hand flat with fingers together and thumb tucked in.",
            "ascii": """
  ____
 |    |
 |____|
"""
        },
        "C": {
            "description": "Curve your hand into a 'C' shape.",
            "ascii": """
   ____
  /    \\
 |      |
  \\____/
"""
        },
    },
    "numbers": {
        "1": {
            "description": "Hold up your index finger.",
            "ascii": """
  |
  |
  |
"""
        },
        "2": {
            "description": "Hold up your index and middle fingers.",
            "ascii": """
  /|
 / |
/  |
"""
        },
        "3": {
            "description": "Hold up your index, middle, and ring fingers.",
            "ascii": """
  /|\\
 / | \\
/  |  \\
"""
        },
    },
    "words": {
        "hello": {
            "description": "Wave your hand.",
            "ascii": """
  👋
 / \\
/   \\
"""
        },
        "thank you": {
            "description": "Place your hand near your chin and move it forward.",
            "ascii": """
  🙏
 /   \\
/     \\
"""
        },
        "goodbye": {
            "description": "Wave your hand like you're saying goodbye.",
            "ascii": """
  👋
 / \\
/   \\
"""
        },
    }
}

@app.route("/", methods=["GET", "POST"])
def learn_sign_language():
    error = None
    result = None

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip().lower()

        if user_input == "learn alphabet":
            result = "Here are the signs for the alphabet:\n"
            for letter, data in signs["alphabet"].items():
                result += f"{letter}: {data['description']}\n{data['ascii']}\n"

        elif user_input == "learn numbers":
            result = "Here's how to sign numbers 1 to 3:\n"
            for number, data in signs["numbers"].items():
                result += f"{number}: {data['description']}\n{data['ascii']}\n"

        elif user_input.startswith("learn"):
            word = user_input.replace("learn", "").strip()
            if word in signs["words"]:
                data = signs["words"][word]
                result = f"The sign for '{word}' is: {data['description']}\n{data['ascii']}"
            else:
                error = f"I don't know the sign for '{word}' yet. Can you teach me?"

        elif user_input.startswith("teach"):
            parts = user_input.split(" ")
            if len(parts) >= 3:
                word = parts[1]
                sign = " ".join(parts[2:])
                signs["words"][word] = {"description": sign, "ascii": "No ASCII art yet."}
                result = f"Thanks! I've learned that '{word}' is signed as '{sign}'."
            else:
                error = "Please use the format: 'teach [word] [sign description]'."

        elif user_input == "quiz me":
            return jsonify({"redirect": "/quiz"})

        else:
            error = "I can help you learn the alphabet, numbers, or quiz you on signs!"

    return render_template("index.html", error=error, result=result)

@app.route("/quiz", methods=["GET"])
def quiz_me():
    quiz_questions = {
        "What is the sign for 'hello'?": "wave hand",
        "What is the sign for 'thank you'?": "place hand near chin and move forward",
        "What is the sign for 'goodbye'?": "wave hand",
    }
    question = random.choice(list(quiz_questions.keys()))
    return jsonify({
        "question": question,
        "hint": "Think about the action!",
        "answer": quiz_questions[question]
    })

if __name__ == "__main__":
    app.run(debug=True)
