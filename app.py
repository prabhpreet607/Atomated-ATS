import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

import os
import PyPDF2 as pdf

genai.configure(api_key=os.getenv("GOOGLE-API"))


def get_gemini(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text


def input_pdf_file(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
        return text


input = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
make sure to leave necessary spaces to make it more readable and 
try not to change the result if called again and again
"""

st.title("ATS resume")
st.text("improve your resume ats")

jd = st.text_area("Paste the Job Description")
upload_file = st.file_uploader("uploade your file", type="pdf", help="please upload a pdf file")

submit = st.button("submit")

if submit:
    if upload_file is not None:
        text = input_pdf_file(upload_file)
        response = get_gemini(input)

        st.subheader(response)