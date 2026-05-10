import requests


def call_llm(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {"model": "qwen2.5:7b", "prompt": prompt, "stream": False}

    response = requests.post(url, json=payload)
    return response.json()["response"]


# -----------------------------
# RUN TEST
# -----------------------------
if __name__ == "__main__":
    metadata = call_llm("Hello")
    print(metadata)
