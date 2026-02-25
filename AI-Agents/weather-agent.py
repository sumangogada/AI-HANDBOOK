import json
import os

import requests
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import logging

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def get_weather(latitude, longitude):
    """This is a publically available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature and weather for provided coordinates (latitude, longitude).",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location.",
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location.",
                    },
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

messages=[
    {"role":"system","content":"Respond client friendly to user request with the weather details of the location."},
    {"role":"user","content":"What is the current weather in paris?"}
]

model = "gpt-4o"

class weather_details_format(BaseModel):
    wind_speed: str = Field(description="Gives the wind speed at the given coordinates. Ex:30km/h")
    elevation: int = Field(description="Gives the elevation . Ex:4365ft")
    date: str = Field(description="gives the date and time of location.")


#That block is a plain chat completion with tools: it sends the conversation and tool definitions and gets 
# back the model’s reply (often a tool call), but it does not:
#Run the tool (get_weather)

completion = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )
  
completion.model_dump() # is a method that turns a Pydantic model instance into a plain Python dict.


def call_function(name,args):
    if name == "get_weather":
      return get_weather(**args)


for tool_call in completion.choices[0].message.tool_calls:
    name= tool_call.function.name
    args = json.loads(tool_call.function.arguments) # turns a JSON string into a Python object.
    messages.append(completion.choices[0].message)

    result = call_function(name,args) #Actual fucntion call is made 

    messages.append(
        {"role":"tool","tool_call_id":tool_call.id,"content":json.dumps(result)} #response is being appended to messages
    )

completion2 = client.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=weather_details_format
)

print(completion2.choices[0].message.parsed)