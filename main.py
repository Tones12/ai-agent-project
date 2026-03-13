import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent-project!")
    
    # API Key Check
    if api_key is None:
        raise RuntimeError("API Key not found")

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="gemini-2.5-flash")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
    # call the model, handle responses, etc.
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0),
        )

        # Determine if response came in
        if response.usage_metadata is None:
            raise RuntimeError("Failed API request")
    
        user_prompt = args.user_prompt
        prompt_count = response.usage_metadata.prompt_token_count
        response_count = response.usage_metadata.candidates_token_count
        response_candidates = response.candidates
        if response_candidates:
            for content in response_candidates:
                messages.append(content.content)

        # If --verbose given:
        if args.verbose is True:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_count}")
            print(f"Response tokens: {response_count}")
        
        function_call_result = None
        function_call_results = []

        # AI API response output
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception("Error: function call results empty")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Error: function response is empty")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Error: no function result")
                function_call_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_call_results))
        else:
            print(response.text)
            return
    print("Maximum iterations reached without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()