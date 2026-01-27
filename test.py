from dotenv import load_dotenv
import os

load_dotenv()
my_variable = os.environ.get('OPENAI_API_KEY')

print(my_variable)




