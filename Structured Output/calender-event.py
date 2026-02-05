import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

class CalenderEvents(BaseModel):
    name:str
    date:str
    participants:list[str]


completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role":"system","content":"Extract the event information"},
            {"role":"user","content":"ALice and Bob are going to science fare on friday"}

        ],
        response_format=CalenderEvents,
)

print(completion.choices[0].message.content)