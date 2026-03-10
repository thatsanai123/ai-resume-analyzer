from flask import Flask, render_template, request
import os
import re
score = 0
import PyPDF2
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.environ["GROQ_API_KEY"])


# ---------- FUNCTION READ PDF ----------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


@app.route("/", methods=["GET", "POST"])
def index():

    result = ""

    if request.method == "POST":

        resume_text = request.form.get("resume_text", "")

        uploaded_file = request.files.get("resume_file")

        # ---------- CHECK IF USER UPLOAD PDF ----------
        if uploaded_file and uploaded_file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)

        # ---------- AI PROMPT ----------
        prompt = f"""
Analyze the following resume.

Return the result in this format:

Score: (number between 0-100)

Skills:
- list skills

Recommended Jobs:
- list jobs

Suggestions:
- list improvements

Resume:
{resume_text}
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