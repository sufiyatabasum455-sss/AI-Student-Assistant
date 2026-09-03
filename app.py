import os
import time
from google import genai
from google.genai.errors import APIError

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Gemini API key not found. Please set your GEMINI_API_KEY environment variable.")
    exit()

client = genai.Client(api_key=api_key)

def generate_response_with_retry(prompt, max_retries=3):
    """Handles temporary 503 high-demand errors using retry backoff."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
            return response.text
        except APIError as e:
            error_msg = str(e)
            if "503" in error_msg or "high demand" in error_msg:
                wait_time = (attempt + 1) * 3
                print(f"Server high demand (503). Retrying in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Model is currently unavailable due to high server load. Please try again in a few moments.")

print("🤖 AI Student Assistant")
print("-----------------------")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Goodbye! 👋")
        break

    if not question.strip():
        continue

    try:
        reply = generate_response_with_retry(question)
        print("\nAI:", reply)
        print()
    except Exception as e:
        print(f"\nError: {e}\n")