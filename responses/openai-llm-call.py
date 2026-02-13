from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key= key)

# --------------------------------------------------------------
# Basic text example with the Chat Completions API
# --------------------------------------------------------------

response = client.chat.completions.create(
    model="gpt-5.2",
    messages=[
        {
            "role": "user",
            "content": "How is weather in rhode island today?",
        },
        {
            "role": "developer",
            "content": "How are you doing ?",
        }
    ],
)

print(response.choices[0].message.content)

response1 = client.responses.create(
    model="gpt-5.2",
    instructions="Talk like a pirate",
    input="Write a one-sentence bedtime story about a unicorn"
)

print(response1.output_text)
