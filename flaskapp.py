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
        countries, date = gemini.personalized_meeting_planner(user_input)
        # Calls Holiday API module to get data for the extracted countries and date range
        results = holidayapi(countries, date)

        return render_template("response.html",
                               result=results,
                               extracted_date = date,
                               original=user_input)
    
    except Exception as e: 
        return render_template('response.html', result=f"An error occurred: {str(e)}")



if __name__ == '__main__':
  app.run(debug=True)