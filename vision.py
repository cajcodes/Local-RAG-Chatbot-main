# Adapted from OpenAI's Vision example 
from openai import OpenAI
import base64
import os

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Ask the user for a path on the filesystem:
path = input("Enter the local path to an image:")

# Read the image and encode it to base64:
base64_image = ""
try:
    with open(os.path.expanduser(path), "rb") as image_file:
        image = image_file.read()
        base64_image = base64.b64encode(image).decode("utf-8")
except FileNotFoundError:
    print("The specified file does not exist. Make sure the path is correct.")
    exit()
except Exception as e:
    print(f"An error occurred while reading the image: {str(e)}")
    exit()

completion = client.chat.completions.create(
    model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
    messages=[
        {
            "role": "system",
            "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image.",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image",
                    "image": base64_image,
                },
            ],
        }
    ],
    max_tokens=1000,
    stream=True
)

for chunk in completion:
    if chunk.choices[0].delta.get("content"):
        print(chunk.choices[0].delta["content"], end="", flush=True)
