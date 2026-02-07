import os
import argparse
from dotenv import load_dotenv 
from google import genai
from google.genai import types
from prompts import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError ("GEMINI_API_KEY environment variable not found")

    #This adds functionality, user adds prompt to command line
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Ai_Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    #Verbose option
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    #This stores messages for the convo
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    
    if not response.usage_metadata:
        raise RuntimeError("failed api request")
    
    
    if args.verbose :
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print(response.text)

    print(response.text)

if __name__ == "__main__":
    main()
