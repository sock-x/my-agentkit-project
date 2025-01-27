import random

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

def quiz_me():
    quiz_questions = {
        "What is the sign for 'hello'?": "wave hand",
        "What is the sign for 'thank you'?": "place hand near chin and move forward",
        "What is the sign for 'goodbye'?": "wave hand",
    }
    question = random.choice(list(quiz_questions.keys()))
    print(question)
    answer = input("Your answer: ")
    if answer.lower() == quiz_questions[question]:
        print("Correct! 🎉")
    else:
        print(f"Try again! The correct answer is: {quiz_questions[question]}")

def learn_sign_language():
    print("Welcome to the Sign Language Learning Bot!")
    print("Type 'help' for a list of commands or 'exit' to quit.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'learn alphabet':
            print("Here are the signs for the alphabet:")
            for letter, data in signs["alphabet"].items():
                print(f"{letter}: {data['description']}")
                print(data['ascii'])  # Display ASCII art
        elif user_input.lower() == 'learn numbers':
            print("Here's how to sign numbers 1 to 3:")
            for number, data in signs["numbers"].items():
                print(f"{number}: {data['description']}")
                print(data['ascii'])  # Display ASCII art
        elif user_input.lower().startswith('learn'):
            word = user_input.lower().replace("learn", "").strip()
            if word in signs["words"]:
                data = signs["words"][word]
                print(f"The sign for '{word}' is: {data['description']}")
                print(data['ascii'])  # Display ASCII art
            else:
                print(f"I don't know the sign for '{word}' yet. Can you teach me?")
        elif user_input.lower() == 'quiz me':
            quiz_me()
        elif user_input.lower().startswith('teach'):
            parts = user_input.lower().split(" ")
            if len(parts) >= 3:
                word = parts[1]
                sign = " ".join(parts[2:])
                signs["words"][word] = {"description": sign, "ascii": "No ASCII art yet."}
                print(f"Thanks! I've learned that '{word}' is signed as '{sign}'.")
            else:
                print("Please use the format: 'teach [word] [sign description]'.")
        elif user_input.lower() == 'help':
            print("Here are the commands you can use:")
            print("- 'learn alphabet': Learn how to sign the alphabet.")
            print("- 'learn numbers': Learn how to sign numbers.")
            print("- 'learn [word]': Learn how to sign a specific word (e.g., 'learn hello').")
            print("- 'quiz me': Test your knowledge of sign language.")
            print("- 'teach [word] [sign]': Teach the bot a new sign.")
            print("- 'exit': Quit the bot.")
        else:
            print("I can help you learn the alphabet, numbers, or quiz you on signs!")

if __name__ == "__main__":
    learn_sign_language()
