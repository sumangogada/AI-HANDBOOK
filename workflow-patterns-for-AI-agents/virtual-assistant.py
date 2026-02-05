from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model = "gpt-4o"

class EventExtractionAndDetail(BaseModel):
    description:str=Field(description="Raw description.")

    is_valid_event:bool=Field(
        description=f"Is the {description} is to 'set alarms, play music, and control smart home devices'. "
    )

    confidence_score:int=Field(description="between 0 and 1")

class EventExecution(BaseModel):
    assistance_response:str=Field(description="Gives the response based on user input.Ex:'set alarms, play music, and control smart home devices'.")


def extract_user_input(user_input:str)->EventExtractionAndDetail:

    logger.info("Inside extract user input.")

    completion= client.beta.chat.completions.parse(

        model=model,
        messages=[
            {
                "role":"system",
                "content":"Be a helpful virtual assistant."
            },
            {
                "role":"user",
                "content":user_input
            }
        ],
        response_format=EventExtractionAndDetail,
    )
    result = completion.choices[0].message.parsed
    logger.info(f"Succesfully completed extracting user input and question is {result.description} ,confidence score is : {result.confidence_score}")
    return result



def event_execution(event_extraction_and_detail:EventExtractionAndDetail)->EventExecution:
     logger.info("Executing event_execution")

     completion = client.beta.chat.completions.parse(
          model=model,
          messages=[
               {
                    "role":"system",
                    "content":"Generate a human readable resposne."
               },
               {
                    "role":"user",
                    "content":str(event_extraction_and_detail.model_dump())
               }
          ],
          response_format=EventExecution
     )
     result = completion.choices[0].message.parsed
     logger.info("Successfully Executed event_execution")

     return result
     

def process_user_request(user_input_val:str)->Optional[EventExecution]:
    
    input_extraction= extract_user_input(user_input_val)

    if(not input_extraction.is_valid_event or
         input_extraction.confidence_score < 0.7):
            logger.warning(f"gate check failed for virtual assistance : {input_extraction.is_valid_event} and confidence score is : {input_extraction.confidence_score}")
            return None

    completion = event_execution(input_extraction)

    print(completion.assistance_response)

    return completion


user_input="which 5 songs you reccommend in bollywood."

result = process_user_request(user_input)

if result:
    print(f"Confirmation: {result.assistance_response}")
  
else:
    print("I's sorry , I cannot assist with this type of request.")