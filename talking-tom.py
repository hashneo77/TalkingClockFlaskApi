from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

def number_to_words(n):
    num_words = {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
        8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
        15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
        21: "twenty-one", 22: "twenty-two", 23: "twenty-three", 24: "twenty-four", 25: "twenty-five",
        26: "twenty-six", 27: "twenty-seven", 28: "twenty-eight", 29: "twenty-nine", 30: "thirty"
    }
    return num_words.get(n, str(n))

def human_friendly_time(hour=None, minute=None):
    if hour is None or minute is None:
        now = datetime.datetime.now()
        hour = now.hour if hour is None else hour
        minute = now.minute if minute is None else minute

    if hour == 0:
        hour = 12
    elif hour > 12:
        hour -= 12

    hour_names = [
        "twelve", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven"
    ]

    if minute == 0:
        return f"{hour_names[hour % 12]} O' Clock"
    elif minute == 15:
        return f"quarter past {hour_names[hour % 12]}"
    elif minute == 30:
        return f"half past {hour_names[hour % 12]}"
    elif minute == 45:
        next_hour = (hour + 1) % 12
        return f"quarter to {hour_names[next_hour]}"
    elif minute < 30:
        return f"{number_to_words(minute)} past {hour_names[hour % 12]}"
    else:
        next_hour = (hour + 1) % 12
        return f"{number_to_words(60 - minute)} to {hour_names[next_hour]}"

# Define an API route that exposes the functionality
@app.route('/time', methods=['GET'])
def get_human_friendly_time():
    # Get 'hour' and 'minute' from request parameters, if provided
    hour = request.args.get('hour', default=None, type=int)
    minute = request.args.get('minute', default=None, type=int)
    if hour is None or minute is None:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
    # Get the human-friendly time
    human_time = human_friendly_time(hour, minute)

    # Return the response as JSON
    return jsonify({
        'human_time': human_time,
        'hour': hour,
        'minute': minute
    })

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
