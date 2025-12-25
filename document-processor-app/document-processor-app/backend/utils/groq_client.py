import requests
import os

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/v1"

    def upload_file(self, file_path):
        url = f"{self.base_url}/upload"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        with open(file_path, 'rb') as file:
            response = requests.post(url, headers=headers, files={"file": file})
        return response.json()

    def process_file(self, file_id):
        url = f"{self.base_url}/process/{file_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.post(url, headers=headers)
        return response.json()

    def get_file_status(self, file_id):
        url = f"{self.base_url}/status/{file_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        return response.json()