from google import genai
from google.genai import types
import os
from pydantic import BaseModel

class CountriesDates(BaseModel):
    countries: list[str]
    month: str 
    scheduling_constraints: str 


api_key = os.getenv("GEMINI_API_KEY") # create environment variable for your API key
        

def get_countries_and_dates(user_input: str):
    """ Identify the countries and date range for the meeting """

    try:
        # Initialize the GenAI client
        client = genai.Client(api_key=api_key)
        # Create the prompt with system instructions and user input
        response = client.models.generate_content(
            # model type
            model="gemini-2.5-flash",
            # the system instructions and user input
            config=types.GenerateContentConfig(
                response_schema=CountriesDates,
                response_mime_type='application/json',
                system_instruction="""
                            You are an AI assistant that helps users plan meetings by analyzing international holidays.
                            
                            Your Responsibilities:

                            Interpret the user’s input and extract:

                            A list of the countries involved (using 2-letter country codes, e.g., US for United States, SG for Singapore, FR for France, etc. If a country name is given, convert it to the corresponding 2-letter code.)

                            The month identified (only reutrn the most likely month)

                            Any scheduling constraints (e.g., weekdays only, avoid Fridays, earliest possible date, flexible schedule, etc.)
        """),
            contents=f"User input: {user_input}",
        )
        
        return response.parsed  # A CountriesDates object 
    
    except Exception as e:
        print( f"An error occurred: {e}")
        return None

    
def propose_meeting_schedule(country_dates, holidays):

    """ Use the Countries and Dates from the earlier call, plus holidays from the API, to propose meeting times """

    try:
        # Initialize the GenAI client
        client = genai.Client(api_key=api_key)
        # Create the prompt with system instructions and user input
        response = client.models.generate_content(
            # model type
            model="gemini-2.5-flash",
            # the system instructions and user input
            config=types.GenerateContentConfig(
                system_instruction="""
                            Your role is:

                            Analyze the holiday data;

                            Identify dates within the user’s range that contain no holidays in any of the countries;

                            Recommend the best available meeting dates with respect to the time zones in the countries given 

                            Provide a concise personalized explanation

       """),
            contents=f"""Countries, dates, scheduling constraints: {country_dates},   
            Holiday Data: {holidays}""",
        )
        
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == '__main__':   # This code will only 
    cd = get_countries_and_dates("Help me plan a meeting between Singapore and France anytime in April. Avoid holidays and try to keep it early in the month.",)
    print(cd)
    schedule = propose_meeting_schedule(cd, [])   # The empty list will be a list of holidays fetched from the API 
    print(schedule)