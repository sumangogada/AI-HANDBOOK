from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model = "gpt-4o"

# --------------------------------------------------------------
# Step 1: Define the data models for each stage
# --------------------------------------------------------------
#Note : These models defins what you need from openai when request is sent.

class EventExtraction(BaseModel):
    description:str=Field(description="Raw description of the event")

    is_calendar_event:bool=Field(
        description="Whether this text describes a calendar event"
    )
    confidence_score:float=Field(description="Confidence score between 0 and 1")

class EventDetails(BaseModel):
        name_of_the_event:str=Field(description="Name of the event")
        date_of_the_event:str=Field(description="Date and time of the event.Use ISO 8601 to format this value.")
        people_attending_the_event:list[str]=Field(description="List of participants")
        duration_in_minutes:int=Field(description="Expected duration in minutes")

class EventDistribution(BaseModel):
      confirmation_message:str=Field(description="Natural language confirmation message")

      calendar_link:Optional[str]=Field(
            description="Generate link if available"
      )

# --------------------------------------------------------------
# Step 2: Define the functions
# --------------------------------------------------------------
#Note: make the openai call 
      
def extract_event_info(user_input:str)->EventExtraction:
      logger.info("Starting event extraction analysis")
      logger.debug(f"Input text: {user_input}")

      today = datetime.today()
      date_context = "Today is {today.strftime(%A, %B %d, %Y')}."
      

      completion = client.beta.chat.completions.parse(
           model=model,
           messages=[
                 {
                       "role":"system",
                       "content":f"{date_context} Analyse if the text describes a calendar event"
                 },
                 {
                       "role":"user",
                       "content":user_input
                 }
           ],
           response_format=EventExtraction,
      )

      result = completion.choices[0].message.parsed
      logger.info(f"is calendar event: {result.is_calendar_event}  and the event is: {result.description} and confidence is {result.confidence_score}")

      return result


def parse_event_information(description:str)->EventDetails:
      
       logger.info("Starting event details parsing")
       today = datetime.today()
       date_context =f"Today is {today.strftime('%A, %B %d, %Y')}."

       completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                  {
                        "role":"system",
                        "content":f"{date_context} Extract detailed information.If a day is mentioned like 'next Tuesday' or similar dates,use this current date as reference."
                  },
                  {
                        "role":"user",
                        "content":description
                  },
                  
            ],
            response_format=EventDetails,
       )
       result = completion.choices[0].message.parsed
       logger.info(f"Reponse recieved and the name of the event is {result.name_of_the_event} and the date of the event is {result.date_of_the_event} ")
       logger.debug(f"Participants: {', '.join(result.people_attending_the_event)}")
       return result

def event_distribution(event_details:EventDetails)->EventDistribution:
      logger.info("Generating confirmation message")

      completion=client.beta.chat.completions.parse(
            model=model,
            messages=[
                  {
                        "role":"system",
                        "content":"Generate a human readable confirmation message.Sign of with your name:Suman"
                  },
                  {
                        "role":"user",
                        "content":str(event_details.model_dump())
                  }
            ],
            response_format=EventDistribution,
      )
      result = completion.choices[0].message.parsed
      logger.info("Cofirmation message generated.")

      return result

# --------------------------------------------------------------
# Step 3: Chain the functions together
# --------------------------------------------------------------\

def process_calendar_request(user_input:str)->Optional[EventDistribution]:
      
    logger.info("Processing calendar request")
    logger.debug(f"Raw input: {user_input}")

    intial_extraction = extract_event_info(user_input)

    if(
          not intial_extraction.is_calendar_event
          or intial_extraction.confidence_score < 0.7
    ):
          logger.warning(f"gate check failed as calendar event : {intial_extraction.is_calendar_event} and confidence score is : {intial_extraction.confidence_score}")

    logger.info("Gate check passed, proceeding with event processing")

    event_details = parse_event_information(intial_extraction.description)

    confirmation = event_distribution(event_details)

    logger.info("Calendar request processing completed successfully")

    return confirmation

# --------------------------------------------------------------
# Step 4: Test the chain with a valid input
# --------------------------------------------------------------

user_input = "Let's schedule a 1hour team meeting next Tuesday at 2pm with Alice and Bob to discuss the project roadmap."

result = process_calendar_request(user_input)

if result:
    print(f"Confirmation: {result.confirmation_message}")
    if result.calendar_link:
        print(f"Calendar Link: {result.calendar_link}")
else:
    print("This doesn't appear to be a calendar event request.")