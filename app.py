import os
from flask import Flask, render_template
from weather import get_weather

app = Flask(__name__)

# Use a secret key if we add forms later; pull from env if set
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-not-secret")

@app.route("/")
def home():
    try:
        data = get_weather()
        return render_template("index.html", weather=data)
    except Exception as e:
        # Show a friendly message instead of crashing
        # (In production, you'd log 'e' to a file, not show it)
        return render_template("index.html", weather={
            "temp": "N/A",
            "description": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=False)
