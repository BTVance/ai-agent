import sys
import os
import argparse
from config import MAX_ITERS
from dotenv import load_dotenv 
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


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
    
    
    for _  in range(MAX_ITERS):
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
    
        if not response.usage_metadata:
            raise RuntimeError("failed api request")
    
    
        if args.verbose :
            print("User prompt:", args.user_prompt)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        if response.candidates:
            for c in response.candidates:
                if c.content: 
                    messages.append(c.content)

        function_calls = response.function_calls

        function_responses = []
        if function_calls:

            for function_call in function_calls:
                result = call_function(function_call, args.verbose)
                if not result.parts:
                    raise RuntimeError()
                if not result.parts[0].function_response:
                    raise RuntimeError()
                if not result.parts[0].function_response.response:
                    raise RuntimeError()
                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")
        
                function_responses.append(result.parts[0])
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print(response.text)
            return
        
    
    print("maximum number of iterations reached without a final response")
    sys.exit(1)
            
                    

if __name__ == "__main__":
    main()

