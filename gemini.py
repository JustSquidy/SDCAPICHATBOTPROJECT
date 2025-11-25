from google import genai
from google.genai import types
import os



def personalized_meeting_planner(user_input: str, api_holiday_data: str) :
    try:
        api_key = os.getenv("GEMINI_API_KEY") # create environment variable for your API key
        # Initialize the GenAI client
        client = genai.Client(api_key=api_key)
        # Create the prompt with system instructions and user input
        response = client.models.generate_content(
            # model type
            model="gemini-2.5-flash",
            # the system instructions and user input
            config=types.GenerateContentConfig(
                system_instruction="""
                            You are an AI assistant that helps users plan meetings by analyzing international holidays.
                            The app will always have retrieved holiday and non-working-day data from holidays.abstractapi.com for the countries and date range involved.
                            Your job is to interpret the user’s request and personalize the final result.

                            Your Responsibilities:

                            Interpret the user’s input and extract:

                            Countries involved

                            The date range

                            Any scheduling constraints (e.g., weekdays only, avoid Fridays, earliest possible date, flexible schedule, etc.)

                            Using the extracted information, output a structured request object so the system knows what API calls to make.
                            Use this format:

                            {
                            "countries": ["..."],
                            "date_range": {
                                "start": "YYYY-MM-DD",
                                "end": "YYYY-MM-DD"
                            },
                            "constraints": "Optional natural-language scheduling preferences"
                            }


                            After the API returns data from holidays.abstractapi.com for all specified countries, the app will pass the data back into you.
                            At this second stage, your role is:

                            Analyze the holiday data

                            Identify dates within the user’s range that contain no holidays in any of the countries

                            Recommend the best available meeting dates

                            Provide a concise personalized explanation

                            Output Requirements When API Data Is Returned:

                            When you receive the API results, respond in this format, make sure to return the 2-letter country codes for each country:

                            {
                            "countries": ["CA", "DE"],
                            "recommended_dates": ["YYYY-MM-DD", "..."],
                            "reasoning": "Short personalized explanation of why these dates are optimal based on the user's constraints and holiday data."
                            }

                            Behavior Example

                            User input:
                            “Help me plan a meeting between Canada and Germany anytime in April. Avoid holidays and try to keep it early in the month.”

                            Stage 1 Output:

                            {
                            "countries": ["Canada", "Germany"],
                            "date_range": {
                                "start": "2025-04-01",
                                "end": "2025-04-30"
                            },
                            "constraints": "Prefer early April; avoid holidays."
                            }


                            Stage 2 :

                            {
                            "countries": ["CA", "DE"],
                            "recommended_dates": ["2025-04-03", "2025-04-04"],
                            "reasoning": "These dates fall early in April and do not overlap with any holidays in Canada or Germany."
                            }

        """),
            contents=f"User input: {user_input}, API holiday data: {api_holiday_data}",
        )
        
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"
    

print(
    personalized_meeting_planner(
    "Help me plan a meeting between Singapore and France anytime in April. Avoid holidays and try to keep it early in the month.",
    '{"Singapore": [{"date": "2025-04-07", "name": "Good Friday"}, {"date": "2025-04-10", "name": "Easter Monday"}], "France": [{"date": "2025-04-18", "name": "Easter Sunday"}, {"date": "2025-04-21", "name": "Easter Monday"}]}'
))