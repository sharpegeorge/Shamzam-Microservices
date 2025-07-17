import requests

API_URL = "https://api.audd.io"

# Read api key
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()  # reads and then removes any spaces or newline characters

def recognise_audio(audio):
    
    payload = {
        "api_token": api_key,
        "audio": audio
    }

    response = requests.post(API_URL, json=payload).json()

    # checking if an error is returned
    #print(response)
    if response['status'] == 'error':
        return {"status": "API request failed", "code": response['error']['error_code']}
    
    # getting results
    if "result" in response and response["result"]:
        return {
            "title": response["result"]["title"],
            "artist": response["result"]["artist"]
        }
    
    # if no result is found
    return {"status": "No match found"}
