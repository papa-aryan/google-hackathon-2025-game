import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key = google_api_key)

textModel = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
# textModel = genai.GenerativeModel("gemini-2.0-flash")


def get_google_joke():
    """Generates and returns a short joke about Google."""
    try:
        googleResponse = textModel.generate_content("You're a world class stand-up comedian. You're standing in front of a crowd with 2500 people. Tell the croud a short joke about Google.")
        return googleResponse.text
    except Exception as e:
        print(f"Error generating joke: {e}")
        return "Could not fetch a joke."

def list_available_models():
    """Prints the names of models that support 'generateContent'."""
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(model.name)
            print()

# This block runs only when apiTest.py is executed directly (not when imported)
if __name__ == "__main__":
    print("Available models:")
    list_available_models()
    
    print("\nFetching a Google joke:")
    joke = get_google_joke()
    print(joke)

    #response2 = textModel.generate_content("Have you read Leopold Aschenbrenner's essay 'Situational Awareness'?")
    # print(response2.text)