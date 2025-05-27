from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key = google_api_key)



reponse2 = client.models.generate_content(
    model="gemini-2.5-flash-preview-05-20",
    contents="Explain how AI works in a few words",
    )


def generate_text_from_input(prompt_text: str, model_name: str = "gemini-2.0-flash"):
    """Generates text using the specified model and prompt."""
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt_text,
        )
        print("the response is:")
        print(response.text)
        return response.text
    except Exception as e:
        print(f"Error generating text: {e}")
        return "Could not generate text."


def get_philosophy_question():
    """Generates and returns a short joke about Google."""
    try:
        response1 = client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents="You are a philosophically inclined AI enthusiast who thinks a very hard about the future and AI. Ask me one deep question that will make me think about the future, AI, humanity or a combination. Keep the language simple. The question should be short and persuasive.",
            #contents="You're a world-class comedian. You're currently standing on a stage at a comedy show in front of 2500 people. Tell the audience a short joke about Google.",
)
        return response1.text
    except Exception as e:
        print(f"Error generating joke: {e}")
        return "Could not fetch a joke."

def list_available_models():
    """Prints the names of available models."""
    print("Listing all available models:")
    try:
        print("Available models:")
        for model in client.models.list():
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {e}")


# This block runs only when apiTest.py is executed directly (not when imported)
if __name__ == "__main__":
    #list_available_models()
    
    print("\nFetching a Google joke:")
    joke = get_philosophy_question()
    print(joke)

    print("\nText from custom input:")
    custom_prompt = "Explain what a transformer is in AI to a student in two sentences."
    generated_answer = generate_text_from_input(custom_prompt)
    print(f"Prompt: {custom_prompt}")
    print(f"Answer: {generated_answer}")


    #response2 = textModel.generate_content("Have you read Leopold Aschenbrenner's essay 'Situational Awareness'?")
    # print(response2.text)