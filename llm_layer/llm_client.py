import requests
from datetime import datetime


def call_llm(prompt):
    # print(prompt)
    url = "http://localhost:11434/api/generate"
    payload = {"model": "qwen2.5:7b", "prompt": prompt, "stream": False}
    response = requests.post(url, json=payload)
    # print(response.json()["response"])
    with open("json.txt", "a") as file:
        file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        file.write(response.json()["response"])
        
    return response.json()["response"]


# -----------------------------
# RUN TEST
# -----------------------------
if __name__ == "__main__":
    metadata = call_llm("Hello")
