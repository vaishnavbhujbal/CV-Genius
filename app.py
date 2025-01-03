from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai
from textblob import TextBlob

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(upload_file):
    if upload_file is not None:
        images = pdf2image.convert_from_bytes(upload_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def analyze_sentiment(resume_text):
    blob = TextBlob(resume_text)
    sentiment = blob.sentiment
    return {'polarity': sentiment.polarity, 'subjectivity': sentiment.subjectivity}


st.set_page_config(page_title="CV Genius")
st.header("CV Genius")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about the resume")
submit2 = st.button("How can I improve my skills")
submit3 = st.button("Percentage match")
submit4 = st.button("Sentiment Analysis")



input_prompt1 = """
You are an experienced Technical Human Resource Manager in the field of any one job role from Data Science, Full Stack Web Developer, Big Data Engineering, DEVOPS, Data Analyst, Software Engineer. Your task is to review the resume against the job description for these profiles, 
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strength and weakness of the application in relation to the specified job requirements.  
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from Data Science, Full Stack Web Developer, Big Data Engineering, DEVOPS, Data Analyst, Software Engineer and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from Data Science, Full Stack Web Developer, Big Data Engineering, DEVOPS, Data Analyst, Software Engineer and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1 or submit2 or submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if submit1:
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
        elif submit2:
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
        else:
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

if submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        resume_text = get_gemini_response("Extract the text from this resume", pdf_content, "")
        sentiment_result = analyze_sentiment(resume_text)
        st.subheader("Sentiment Analysis:")
        st.write(f"**Polarity: {sentiment_result['polarity']}**<br>Ranges from: -1 to +1  <br><br>", unsafe_allow_html=True)
        st.write(f"**Subjectivity: {sentiment_result['subjectivity']}**<br>Ranges from: -1 to +1  ", unsafe_allow_html=True)

    else:
        st.write("Please upload the resume")




