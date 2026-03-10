from flask import Flask, render_template, request
import os
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.environ["GROQ_API_KEY"])

@app.route("/", methods=["GET", "POST"])
def index():

    result = ""

    if request.method == "POST":

        resume = request.form["resume"]

        prompt = f"""
        Analyze this resume and provide:

        1. Skills
        2. Recommended Jobs
        3. Suggestions

        Resume:
        {resume}
        """

        response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

        result = response.choices[0].message.content

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)