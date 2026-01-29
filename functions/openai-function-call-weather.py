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
             {"role":"user","content":"What is the current weather in cumberland,ri?"}
         ]

)

output = completion.choices[0].message.content

print(output)

function_description=[
    {
       "name":"get_weather",
       "description":"Get the current weather of the location",
       "parameters" :{
           "type":"object",
           "properties":{
               "city":{
                   "type":"string",
                   "description":"Weather of the city,e.g. Cumberland"
               },
               "state":{
                   "type":"string",
                   "description":"Weather of the state,e.g. RI"
               }
           },
           "required":["city","state"]
       }
    }
]

def get_weather(city,state):

    weather_details={
            "city":city,
            "state":state,
            "RealFeel":29,
            "RealFeel Shade":23,
            "Max UV Index":"2.0 (Low)",
            "Wind":"WNW 5 mph"
    }
    return json.dumps(weather_details)

user_prompt = "What is the current weather in boston,Mas?"

completion = openai.chat.completions.create(
         model="gpt-3.5-turbo",
         messages=[
             {"role":"user","content":user_prompt},
             
         ],
         functions=function_description,
         function_call="auto"
)

output=completion.choices[0].message
print("Output is :")
print(output)



params = json.loads(output.function_call.arguments)

chosen_function = eval(output.function_call.name)
weather = chosen_function(**params)

print(weather)

second_completion=openai.chat.completions.create(
        model="gpt-3.5-turbo",
         messages=[
            {"role":"user","content":user_prompt},
            {"role":"function","name":output.function_call.name,"content":weather},
         ],
         functions=function_description
)
response = second_completion.choices[0].message.content
print(response)
