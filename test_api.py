import base64
import requests
import json

# --- CONFIGURATION ---
# Replace this with the actual Invoke URL provided by AWS API Gateway
API_ENDPOINT = "https://your-api-id.execute-api.us-east-1.amazonaws.com/analyze-voice"

# Path to the audio file you want to test (e.g., from your dummy data)
AUDIO_FILE_PATH = "data/synthetic_speech/fake_0.wav" 

def test_forensics_api(file_path, url):
    print(f"Loading audio file: {file_path}")
    
    try:
        # 1. Read the audio file as binary
        with open(file_path, "rb") as audio_file:
            binary_audio_data = audio_file.read()

        # 2. Encode the binary data to a Base64 string
        print("Encoding audio to Base64...")
        base64_encoded_audio = base64.b64encode(binary_audio_data).decode('utf-8')

        # 3. Construct the JSON payload required by your Lambda function
        payload = {
            "audio_base64": base64_encoded_audio
        }

        # 4. Send the POST request to the API
        print(f"Transmitting to Cloud API: {url}")
        response = requests.post(
            url, 
            json=payload, 
            headers={"Content-Type": "application/json"}
        )

        # 5. Output the results
        if response.status_code == 200:
            print("\n--- API RESPONSE SUCCESS ---")
            # Pretty-print the JSON response
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"\n--- API ERROR (Status {response.status_code}) ---")
            print(response.text)

    except FileNotFoundError:
        print(f"Error: Could not find the file at {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_forensics_api(AUDIO_FILE_PATH, API_ENDPOINT)