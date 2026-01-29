import os
import json
import openai
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ChatMessage

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')

completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
       messages=[
            {"role":"user","content":"When's the next flight from boston to london?"},
        ],
)
output = completion.choices[0].message.content 
print(output)

function_descriptions = [
    {
        "name":"get_flight_info",
        "description":"Get flight information between two locations",
        "parameters":{
            "type":"object",
            "properties":{
                "loc_origin":{
                    "type":"string",
                    "description":"The departure airport,e.g. BOS",
                },
                "loc_destination":{
                    "type":"string",
                    "description":" The arrival airport,e.g. LHR",
                },
            },
            "required":["loc_origin","loc_destination"]
        },
    }
]

user_prompt = "When's the next flight from denver to luxembourg?"

completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"user","content":user_prompt},
        ],
        functions=function_descriptions,
        function_call="auto",
)

output = completion.choices[0].message
print("Output is :")
print(output) 
 #Not the above function is not yet exist yet beucase we have not created the actual method "get_flight_info" , we just defined the singature of the method and passed to openai


def get_flight_info(loc_origin,loc_destination):
    
    # Assuming this is the output from an api or db
    flight_info = {
        "loc_origin":loc_origin,
        "loc_destination":loc_destination,
        "datetime":str(datetime.now() + timedelta(hours=2)),
        "airline":"virgin atlantic",
        "flight":"VA5135",
    }
    return json.dumps(flight_info)


origin = json.loads(output.function_call.arguments).get('loc_origin')
destination = json.loads(output.function_call.arguments).get('loc_destination')
params = json.loads(output.function_call.arguments)

print(origin)
print(destination)
print(params)

chosen_function = eval(output.function_call.name)
flight = chosen_function(**params)

print(flight)

second_completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"user","content":user_prompt},
        {"role":"function","name":output.function_call.name,"content":flight},
    ],
    functions=function_descriptions
)

response = second_completion.choices[0].message.content
print(response)