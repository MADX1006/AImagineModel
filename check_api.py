# Save this file as check_api.py
import google.generativeai as genai
import sys

# Replace this with your actual API key
# The API key has been updated as requested.
api_key = "AIzaSyCHZa7s34WE-W7VmqdtRPb5hZ4LNe8Wg_c"

try:
    # Configure the API key
    genai.configure(api_key=api_key)

    # Make a simple test call to the Gemini API
    print("Attempting to connect to the Gemini API...")
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
    response = model.generate_content("Hello, how are you?")

    # If the call is successful, print the response text
    print("\n--- Connection Successful! ---")
    print(f"API Response: {response.text}")
    
except Exception as e:
    # If the call fails, print the full error message
    print("\n--- Connection Failed ---", file=sys.stderr)
    print(f"An error occurred: {e}", file=sys.stderr)
    print("\nCommon reasons for failure:", file=sys.stderr)
    print("1. Incorrect API key: Double-check for typos or missing characters.", file=sys.stderr)
    print("2. Network issues: Ensure you have an active internet connection.", file=sys.stderr)
    print("3. Quota limits: You may have exceeded your usage limits.", file=sys.stderr)
