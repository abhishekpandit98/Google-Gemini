import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt = """
Dear Expert Resume Enhancer,

Your expertise in ATS (Application Tracking System) resume enhancement, especially within the technology sector encompassing software engineering, data science, data analysis, and big data engineering, is highly valued. In this task, you are entrusted with evaluating a resume against a provided job description, considering the fiercely competitive job market. Your goal is to offer top-notch assistance in aligning the resume with the job description to enhance its effectiveness.

Assessment Criteria:

1. **Alignment with Job Description**:
   - Analyze the resume's alignment with the provided job description.
   - Assign a percentage match based on how well the resume matches the JD.
   - Identify missing keywords with precision.

2. **Impact Evaluation**:
   - Evaluate the resume's impact by assessing:
     - Quantified achievements
     - Repetition of information
     - Use of strong verbs and appropriate verb tenses
     - Clarity of responsibilities
     - Spelling and grammatical consistency

3. **Brevity and Clarity**:
   - Review the resume for brevity and clarity by considering:
     - Length of the document
     - Usage and effectiveness of bullet points
     - Total number and length of bullets
     - Elimination of unnecessary filler words

4. **Writing Style**:
   - Scrutinize the writing style for:
     - Appropriate use of buzzwords
     - Consistency in date formatting
     - Accuracy and professionalism in contact and personal details
     - Readability, avoiding jargon and complexity
     - Proper use of personal pronouns and active voice
     - Consistency in language and tone

5. **Section Evaluation**:
   - Review the resume sections such as:
     - Education
     - Identification and elimination of unnecessary sections
     - Listing and presentation of skills, including soft and hard skills

Resume Content:
{text}

Job Description:
{jd}

Please provide a detailed report encompassing the following aspects:
- Percentage match with the JD
- List of missing keywords
- Summary of the profile
- Recommendations for improvement
- Assessment of impact
- Assessment of brevity
- Evaluation of writing style
- Feedback on resume sections
"""

## streamlit app
st.title("Score My Resume")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)
       