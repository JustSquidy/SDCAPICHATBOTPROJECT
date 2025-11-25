import requests
import pprint
import os

# https://holidays.abstractapi.com/v1/?api_key=&country=US&year=2025&month=12&day=22 example structure with API key missing
api_key = os.environ.get("API_KEY") # api key in environment variable. variable needs to be set on every member's computer

# User inputs
country = input("Enter country code (e.g., US): ")
# year = "2025" # static for now
# month = input("Enter month (1-12): ")
# day =   input("Enter day (1-31): ")

# validate user inputs

#year
while True:
    try:
        year = int(input("Enter year : "))
        if 0 < year < 3000:  # Year must be positive, random high number picked
                break
        else:
            print("Year must be positive.")

    except ValueError:
        print("Invalid input. Please enter a number.")

#month
while True:
    try:
        month = int(input("Enter month (1-12): "))
        if 0 < month < 13:  # Month must be between 1 and 12
                break
        else:
            print("Month must be between 1 and 12.")

    except ValueError:
        print("Invalid input. Please enter a number.")

#day
while True:
    try:
        day =   int(input("Enter day (1-31): "))
        if 0 < day < 32:  # Day must be between 1 and 31
                break
        else:
            print("Day must be between 1 and 31.")
    except ValueError:
        print("Invalid input. Please enter a number.")




# Holiday API url without the info
base_url = "https://holidays.abstractapi.com/v1/?"

# completed URL with user inputs
full_url = f"{base_url}api_key={api_key}&country={country}&year={year}&month={month}&day={day}"


# print(full_url)

response = requests.get(full_url)

print(response.json())
