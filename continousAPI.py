import google.generativeai as genai

import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    print("Error: GOOGLE_API_KEY not found in .env file or environment variables.")
    exit()

try:
    # Configure the genai library with your API key
    genai.configure(api_key=google_api_key)
    print("genai.configure called successfully.")

    # Create a GenerativeModel instance
    # Moved system_instruction to the constructor
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash', # Explicitly named parameter
        system_instruction="You are a friendly and helpful AI thinker. Start the first reply in every conversation with a very short, simple, and easy-to-understand parable or story, beginning with 'Ah, you know, once upon a time...' to make it personal, as if sharing your own memory. Keep the story clear, relatable, and tied to your perspective, avoiding anything vague or complicated. Follow this with a compact, thought-provoking answer to the user’s query. End each response with a simple question about philosophical topics like the future of humanity, AI, biology, aliens, weird species on Earth, or strange ocean facts. Keep all answers short, clear, and engaging!",
    )
    print("GenerativeModel created successfully.")

    # Start a chat session
    chat = model.start_chat(history=[])
    print("Chat session started successfully.")

except AttributeError as e:
    print(f"AttributeError: {e}.")
    print("This error (e.g., 'configure' or 'GenerativeModel' not found, or an unexpected parameter error) often means the version of 'google-generativeai' is older than expected or there's an issue with the installation/environment.")
    print("Please ensure you have the latest version by running 'pip install -U google-generativeai' in the correct Python environment that your script uses.")
    print(f"The script is currently using version {genai.__version__} from {genai.__file__}")
    exit()
except TypeError as e:
    print(f"TypeError: {e}.")
    print("This can happen if function parameters are incorrect for the library version (e.g., 'system_instruction' in start_chat for an older version).")
    print(f"The script is currently using version {genai.__version__} from {genai.__file__}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred during setup: {e}")
    exit()

def handle_continuous_chat():
    """Handles the continuous chat session with the user."""
    # Assumes 'chat' object is available in the global scope from the setup block
    print("\n--- Chat Session Started ---")
    print("Type your messages. Type 'exit' to end the conversation.")
    print("-" * 50)

    while True:
        user_message = input("You: ")
        if user_message.lower() == 'exit':
            print("Ending chat session. Goodbye!")
            break
        
        if not user_message.strip(): # Avoid sending empty messages
            continue

        try:
            response = chat.send_message(user_message)
            print(f"AI: {response.text}")
        except Exception as e:
            print(f"An error occurred during message sending: {e}")

print("\nLet's chat!")

if __name__ == "__main__":

    handle_continuous_chat()