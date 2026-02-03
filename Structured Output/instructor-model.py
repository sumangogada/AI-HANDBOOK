import os
from dotenv import load_dotenv
import instructor
from pydantic import BaseModel,Field
from openai import OpenAI
from enum import Enum


load_dotenv()

client = instructor.from_openai(OpenAI(api_key=os.environ.get('OPENAI_API_KEY')))

class Reply(BaseModel):
    content :str = Field(description="Your reply that we send to the customer.")
    category:str = Field(description="Category of ticket:'general','order','billing'")


query="Hi there,I have a question about my bill.Can you help me?"

reply=client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Reply,
    messages=[
        {
            "role":"system",
            "content":"Your're a helpful customer care assistant"
        },
        {
            "role":"user",
            "content":query
        }
    ]
)

print(reply.content)

#--------------------------------
