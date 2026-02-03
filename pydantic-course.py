from pydantic import BaseModel,ValidationError

#Pydantic is smart enough to convert a number defined as string to convert to number. Example : age="30" if defined as integer
class User(BaseModel):
    name:str
    age:int
    email:str
try:
    user = User(name="Suman",age="30",email='test@gmail.com')
except ValidationError as e:
    print(e)

print(user.age)
print(user.email) 

used_dict=user.model_dump()
 #Converts an object to dictionary
print(used_dict["name"])

used_dict_json= user.model_dump_json()
#Converts an object to json
print(used_dict_json)
#----------------------------------

class WeatherResponse(BaseModel):
    city:str
    temperature:float
    humidity:int
    description:str

#Simulating api response
api_data={
        "city":"Boston",
        "temperature":18.5,
        "humidity":75,
        "description":"Partly Cloudy"
    }

weather = WeatherResponse.model_validate(api_data)

print(f"Weather in {weather.city}: {weather.temperature}")
