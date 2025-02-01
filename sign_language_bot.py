import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('sign_language.db')
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

# Insert some sample data into the signs table
sample_data = [
    ('hello', 'https://www.youtube.com/watch?v=OcKefCuXyXI', 'Wave your hand with your palm facing outward'),
    ('goodbye', 'https://example.com/goodbye-sign', 'Wave your hand with your palm facing inward'),
    ('thank you', 'https://example.com/thank-you-sign', 'Make a flat "O" shape with your hand and move it away from your body'),
    ('yes', 'https://example.com/yes-sign', 'Nod your head up and down'),
    ('no', 'https://example.com/no-sign', 'Shake your head from side to side')
]

cursor.executemany("INSERT OR IGNORE INTO signs (name, video, description) VALUES (?, ?, ?)", sample_data)

# Commit the changes
conn.commit()

def get_sign_data(sign_name):
    cursor.execute("SELECT * FROM signs WHERE name = ?", (sign_name,))
    result = cursor.fetchone()
    return result

def learn_sign_language():
    print("Welcome to the Sign Language Learning Bot!")
    print("Type 'exit' to quit.")
    print("\nAvailable commands:")
    print("- learn alphabet")
    print("- quiz me")
    print("- what is the sign for [word]")
    print("- practice signs")
    print("- learn phrases")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        # Provide basic responses
        if user_input.lower() == 'learn alphabet':
            print("Here's a video to learn the sign language alphabet: https://example.com/sign-language-alphabet")
        elif user_input.lower() == 'quiz me':
            quiz_me()
        elif user_input.lower().startswith('what is the sign for'):
            get_sign(user_input)
        elif user_input.lower() == 'practice signs':
            practice_signs()
        elif user_input.lower() == 'learn phrases':
            learn_phrases()
        else:
            print("I can help you learn the alphabet or quiz you on signs!")
            print("Try one of the available commands listed above.")

def quiz_me():
    # Select a random sign from the database
    cursor.execute("SELECT name, description FROM signs ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    sign, description = result
    print(f"\nWhat is the sign for '{sign}'?")
    print("(Type your description of the sign)")
    answer = input("\nYou: ").lower()
    
    print(f"\nThe correct sign for '{sign}' is:")
    print(description)
    input("\nPress Enter to continue...")

def get_sign(user_input):
    # Extract the sign from the user's input
    words = user_input.split()
    sign_name = words[-1]
    result = get_sign_data(sign_name)
    
    if result:
        print(f"The sign for '{sign_name}' is: {result[3]}")
        print(f"Video: {result[2]}")
    else:
        print(f"Sorry, I don't know the sign for '{sign_name}' yet.")

def practice_signs():
    print("\nLet's practice some signs!")
    cursor.execute("SELECT name, description FROM signs ORDER BY RANDOM() LIMIT 3")
    practice_signs = cursor.fetchall()
    
    for sign in practice_signs:
        print(f"\nPractice the sign for '{sign[0]}':")
        print(f"Description: {sign[1]}")
        input("Press Enter when you're ready for the next sign...")
    
    print("\nGreat practice session!")

def learn_phrases():
    phrases = [
        "Hello, how are you?",
        "Nice to meet you",
        "Have a good day",
        "Thank you very much"
    ]
    
    print("\nHere are some common phrases to learn:")
    for phrase in phrases:
        print(f"\nPhrase: {phrase}")
        words = phrase.lower().split()
        cursor.execute("SELECT name, description FROM signs WHERE name IN ('hello', 'thank', 'good', 'nice')")
        related_signs = cursor.fetchall()
        if related_signs:
            print("Related signs you already know:")
            for sign in related_signs:
                print(f"- {sign[0]}: {sign[1]}")
        input("\nPress Enter to continue...")
    
    print("\nYou've completed the phrases lesson!")

if __name__ == "__main__":
    try:
        learn_sign_language()
    finally:
        # Close the connection when finished
        conn.close()
