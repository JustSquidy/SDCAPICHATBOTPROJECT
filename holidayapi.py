import requests
import pprint
import os
from datetime import date 

# https://holidays.abstractapi.com/v1/?api_key=&country=US&year=2025&month=12&day=22 example structure with API key missing
api_key = os.environ.get("API_KEY") # api key in environment variable. variable needs to be set on every member's computer


def get_holiday_for_country_and_date(country, month):

    return ['May 4', 'May 30']   # Making up data since I don't have an API key. Remove and use a real API call 

    # !! I haven't tested this. You'd need to make sure it works with the API.
    # I removed the day parameter, since you need all the holidays in a range of dates
    # you may need to make two requests if the user says they want a meeting around the end of a month but the next month is ok too

    # Holiday API url without the info
    base_url = "https://holidays.abstractapi.com/v1/?"

    # assume current year 
    year = date.today().year

    # completed URL with user inputs
    full_url = f"{base_url}api_key={api_key}&country={country}&year={year}&month={month}"

    # print(full_url)

    try:
        response = requests.get(full_url)

        print(response.json())
        return response.json(), None 
    except: 
        return None, 'Error making request to Holiday API'