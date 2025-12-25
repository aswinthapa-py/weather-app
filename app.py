from flask import Flask,render_template,request,session,redirect
from utils.weather_service import get_weather
from datetime import datetime,timedelta

app=Flask(__name__)
app.secret_key="super_secret_key"


def format_datetime(timestamp, timezone):
    utc_time = datetime.utcfromtimestamp(timestamp)
    local_time = utc_time + timedelta(seconds=timezone)
    return local_time.strftime("%A, %B %d, %Y at %I:%M %p")
@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    has_searched = session.get("has_searched", False)

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            weather = get_weather(city, units="metric")

            if weather:
                # ✅ mark search ONLY when successful
                session["has_searched"] = True
                session["last_city"] = city

                weather["datetime"] = format_datetime(
                    weather["timestamp"],
                    weather["timezone"]
                )
            else:
                error = "City not found. Please enter a valid city name."
        else:
            error = "Please enter a city name."

    else:
        if has_searched:
            city = session.get("last_city")
            if city:
                weather = get_weather(city, units="metric")

                if weather:
                    weather["datetime"] = format_datetime(
                        weather["timestamp"],
                        weather["timezone"]
                    )

    return render_template(
        "index.html",
        weather=weather,
        error=error,
        has_searched=session.get("has_searched", False)
    )

@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")
if __name__=="__main__":
    app.run(debug=True)