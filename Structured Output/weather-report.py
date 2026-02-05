import json
import os

import requests
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


def get_weather(latitude, longitude):
    """This is a publically available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]

tools =[
   {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

messages=[
    {"role":"system","content":"Return the weather report"},
    {"role":"user","content":"What's the weather in boston today?"}
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

completion.model_dump()

def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)
    
for tool_call in completion.choices[0].message.tool_calls:
    name=tool_call.function.name
    args= json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, args)   #Actual fucntion call is made 

    messages.append(
        {"role":"tool","tool_call_id":tool_call.id,"content":json.dumps(result)}  #response is being appended to messages
    )


#Once we get the response from weather api now we want to restructure the response to the requestor needs
class WeatherResponse(BaseModel):
    temperature:float = Field(
        description="Get the temperature of the location"
    )
    response:str = Field(
        description="Response in a string format"
    )

completion2 = client.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=WeatherResponse
)

print(completion2.choices[0].message.parsed)