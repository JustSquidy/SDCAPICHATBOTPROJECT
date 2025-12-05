from flask import Flask
from flask import request, render_template
import gemini
import holidayapi

app = Flask(__name__)


@app.route('/')   # home page 
def index():
    return render_template('index.html')   # Show a form for user to type in their request


@app.route('/plan_meeting', methods=['POST']) 
def get_best_times():
    user_input = request.form.get("prompt", "").strip()

    if not user_input:
        return render_template('response.html', result="Please type your request first.")
    
    try: 
        # Asks Gemini to extract countries and date range from user input
        countries_dates = gemini.get_countries_and_dates(user_input)
        print('First Gemini call returned these countries and dates', countries_dates)

        # Calls Holiday API module to get data for the extracted countries and date range
        all_holidays = {}  # Make a dictionary to store the country and the associated holiday 
        for country in countries_dates.countries:
            holidays = holidayapi.get_holiday_for_country_and_date(country, countries_dates.month)  
            all_holidays[country] = holidays

        print('All holidays', all_holidays)

        # Second Gemini call 
        results = gemini.propose_meeting_schedule(countries_dates, all_holidays)

        print('Second Gemini call results', results)

        return render_template("response.html",
                               results=results,
                               original=user_input)
    
    except Exception as e: 
        return render_template('response.html', result=f"An error occurred: {str(e)}")



if __name__ == '__main__':
  app.run(debug=True)