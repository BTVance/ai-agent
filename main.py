import os
import argparse
from dotenv import load_dotenv 
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError ("GEMINI_API_KEY environment variable not found")

    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Ai_Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=args.user_prompt,
    )
    
    if not response.usage_metadata:
        raise RuntimeError("failed api request")
   
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    print(response.text)

if __name__ == "__main__":
    main()
