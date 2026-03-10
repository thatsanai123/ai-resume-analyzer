from flask import Flask, render_template, request
import os
import PyPDF2
from groq import Groq

app = Flask(__name__)

# ---------- LOAD API KEY ----------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=GROQ_API_KEY)


# ---------- FUNCTION READ PDF ----------
def extract_text_from_pdf(file):
    text = ""

    try:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    except Exception as e:
        print("PDF Error:", e)

    return text


# ---------- MAIN PAGE ----------
@app.route("/", methods=["GET", "POST"])
def index():

    result = ""

    if request.method == "POST":

        resume_text = request.form.get("resume_text", "")
        uploaded_file = request.files.get("resume_file")

        # ---------- IF USER UPLOAD PDF ----------
        if uploaded_file and uploaded_file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)

        # ---------- CHECK EMPTY ----------
        if not resume_text.strip():
            result = "Please paste resume text or upload a PDF."
            return render_template("index.html", result=result)

        # ---------- AI PROMPT ----------
        prompt = f"""
Analyze the following resume and provide:

Skills:
- list skills

Recommended Jobs:
- list jobs

Suggestions:
- list improvements

Resume:
{resume_text}
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result = response.choices[0].message.content

        except Exception as e:
            result = f"AI Error: {str(e)}"

    return render_template("index.html", result=result)


# ---------- RUN APP ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)