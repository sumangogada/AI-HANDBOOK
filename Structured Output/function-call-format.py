from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


def send_reply(message: str):
    print(f"Sending reply: {message}")


# --------------------------------------------------------------
# Structured output example using function calling
# --------------------------------------------------------------

query = "Hi there, I have a question about my bill. Can you help me?"

function_name = "chat"

tools = [
    {
        "type": "function",
        "function": {
            "name": function_name,
            "description": f"Function to respond to a customer query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Your reply that we send to the customer.",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["general", "order", "billing"],
                        "description": "Category of the ticket.",
                    },
                },
                "required": ["content", "category"],
            },
        },
    }
]

messages = [
    {
        "role": "system",
        "content": "You're a helpful customer care assistant that can classify incoming messages and create a response.",
    },
    {
        "role": "user",
        "content": query,
    },
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": function_name}},
)

tool_call = response.choices[0].message.tool_calls[0]
type(
    tool_call
)  # openai.types.chat.chat_completion_message_tool_call.ChatCompletionMessageToolCall

function_args = json.loads(tool_call.function.arguments)
type(function_args)  # dict

print(function_args["category"])
send_reply(function_args["content"])