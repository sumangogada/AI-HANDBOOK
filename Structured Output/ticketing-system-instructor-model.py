import instructor
from pydantic import BaseModel,Field
from openai import OpenAI
from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

client = instructor.from_openai(OpenAI(api_key=os.environ.get('OPENAI_API_KEY')))

class TicketCategory(str,Enum):
    GENERAL="general"
    ORDER= "order"
    BILLING = "billing"

class CustomerSentiment(str,Enum):
    NEGATIVE="negative"
    POSITIVE="positive"
    NEUTRAL="neutral"


class Ticket(BaseModel):
    reply:str=Field(description="Your reply tha we send to customer.")
    category:TicketCategory
    confidence:float = Field(ge=0,le=1)
    sentiment:CustomerSentiment

def processTicket(customer_message:str)->Ticket:
    reply = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=Ticket,
        max_retries=3,
        messages=[
            {"role":"system","content":"Analyze the incoming customer message and predict the values for the ticket."},
            {"role":"user","content":customer_message}
        ]
    )

    return reply

ticket = processTicket("Hi there, I have a question about my bill. Can you help me?")
assert ticket.category == TicketCategory.BILLING

print(ticket.reply)
print(ticket.category)
print(ticket.confidence)
print(ticket.sentiment)