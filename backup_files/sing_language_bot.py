def learn_sign_language():
    print("Welcome to the Sign Language Learning Bot!")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        # Provide basic responses
        if user_input.lower() == 'learn alphabet':
            print("Here's a video to learn the sign language alphabet: 
[link]")
        elif user_input.lower() == 'quiz me':
            print("What is the sign for 'hello'?")
            # Add more interactive content here
        else:
            print("I can help you learn the alphabet or quiz you on 
signs!")

if __name__ == "__main__":
    learn_sign_language()
