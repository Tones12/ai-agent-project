import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions


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

    # If --verbose given:
    if args.verbose is True:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_count}")
        print(f"Response tokens: {response_count}")

    # AI API response output
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
        return
    else:
        print(response.text)


if __name__ == "__main__":
    main()