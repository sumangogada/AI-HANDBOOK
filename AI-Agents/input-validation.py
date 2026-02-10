import json
import os

import requests
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

#Vlidate what type of input prompt is given by the user:

class input_validate(BaseModel):
    input:Literal['question','request','complaint']
    confidence_score:int=Field(description='range in between 0 to 1')
    input_str:str=Field(description='Capture the input string given by the user.')

class input_is_question(BaseModel):
    is_question_answered:bool=Field(description='Gives the value if the question is answered or not in YES or NO')
    reasoning:str=Field(description='Give the reason why the question was answered specifically')

class input_is_request(BaseModel):
    reasoning:str=Field(description='Give the reason why the question was answered specifically')

class input_is_complaint(BaseModel):
    reasoning:str=Field(description='Give the reason why the question was answered specifically')
    type_of_complaint:Literal['moderate','severe']


def is_validate(input_str:str)->input_validate:

    response = client.beta.chat.completions.parse(
        model='gpt-4o',
        messages=[
            {
                "role":"system",
                "content":"Validate the type of input . Ex:'question','request' or 'complaint'"
            },
            {
                "role":"user",
                "content":input_str
            }
        ],
        response_format=input_validate
    )
    
    result = response.choices[0].message.parsed
    return result

def is_question(input_str:str)->input_is_question:
    response = client.beta.chat.completions.parse(
        model='gpt-4o',
        messages=[
            {
                "role":"system",
                "content":"Validate the type of input . Ex:'question','request' or 'complaint'"
            },
            {
                "role":"user",
                "content":input_str
            }
        ],
        response_format=input_is_question
    )
    
    result = response.choices[0].message.parsed
    print(result)

def is_request(input_str:str)->input_is_request:
    response = client.beta.chat.completions.parse(
        model='gpt-4o',
        messages=[
            {
                "role":"system",
                "content":"Validate the type of input . Ex:'question','request' or 'complaint'"
            },
            {
                "role":"user",
                "content":input_str
            }
        ],
        response_format=input_is_request
    )
    
    result = response.choices[0].message.parsed
    print(result)



def is_complaint(input_str:str)->input_is_complaint:
    response = client.beta.chat.completions.parse(
        model='gpt-4o',
        messages=[
            {
                "role":"system",
                "content":"Validate the type of input . Ex:'question','request' or 'complaint'"
            },
            {
                "role":"user",
                "content":input_str
            }
        ],
        response_format=input_is_complaint
    )
    
    result = response.choices[0].message.parsed
    print(result)

def process_request(input:str):

    request_type = is_validate(input)

    print(f"Request is : {request_type.input} and the confidence score is : {request_type.confidence_score}")
      
    print(f'input given by the user:{request_type.input_str}')

    if(request_type.input == 'question'):
        is_question(request_type.input_str)
    elif(request_type.input == 'request'):
        is_request(request_type.input_str)
    elif(request_type.input == 'complaint'):
        is_complaint(request_type.input_str)
    else:
        print("Invalid Input!!!")



#process_request("Tell me a joke")
#process_request("What is the best book you recommend for reading?")
#process_request("Iam not happy with your service")