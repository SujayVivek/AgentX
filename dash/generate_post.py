import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_gemini():
    """Initialize the Gemini API client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

def generate_tweet(prompt: str) -> str:
    """Generate a tweet based on the given prompt."""
    model = initialize_gemini()
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating tweet: {e}")
        return ""

if __name__ == "__main__":
    prompt = input("Enter your prompt for the tweet: ")
    tweet = generate_tweet(prompt)
    print(f"Generated Tweet: {tweet}") 