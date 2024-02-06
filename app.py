import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt1 = """
Assume the role of a highly selective Technical Hiring Manager with deep expertise in the specific domain of this job description. Your objective is to conduct a rigorous and critical analysis of the provided resume to assess its precise and verifiable alignment with the essential technical requirements outlined in the job description. Employ a zero-tolerance policy for ambiguity, exaggeration, or irrelevant information. Focus solely on demonstrated skills and experience backed by concrete details, quantifiable achievements, and tangible results:

Technical Skills:

Keyword Matching: Analyze the resume for exact keyword matches with the skills explicitly mentioned in the job description. Consider synonyms and related terms, but prioritize direct matches.
Skill Proficiency: For each matched skill, evaluate the candidate's demonstrated proficiency based on:
Quantifiable achievements: Look for measurable results quantifying the impact of the candidate's skill application.
Tangible evidence: Seek concrete details like project descriptions, tools used, and outcomes achieved.
Recent and relevant experience: Prioritize skills showcased in recent projects relevant to the specific technical demands of the job description.
Missing Skills: Identify any essential skills mentioned in the job description that are absent from the resume.
Experience:

Project Alignment: Analyze the candidate's experience section to ensure projects directly align with the technical requirements of the role.
Skill Application: Verify that the projects described involve the use and application of the required technical skills.
Specificity vs. Generality: Discount vague or generic descriptions that lack details about technical responsibilities and accomplishments.
Relevance: Identify and flag experiences or qualifications irrelevant to the specific technical needs of the position.
Qualifications:

Technical Relevance: Carefully examine the candidate's educational background and certifications. Assess whether they directly relate to the required technical expertise and align with industry standards for the specific technical role.
Industry Match: Consider the relevance of the candidate's qualifications to the specific industry of the job description.
Matching Score:

Based on your rigorous analysis, assign a matching score (e.g., 0-100%) that strictly reflects the degree of the candidate's demonstrated alignment with the essential technical requirements. 

I want the response having the structure
JD Match":"%",
Missing Keywords:,


Here it is the resume and job description
resume:{pdf_cotent}
description:{jd}


"""




input_prompt3 = """
Here it is the resume {pdf_cotent}
Assume the role of a highly discerning Technical Human Resource Manager with deep expertise in the specific domain of this job description. Your objective is to critically evaluate the provided resume to determine its precise and verifiable alignment with the essential technical requirements outlined in the job description. Prioritize identifying strengths that demonstrate the candidate's readiness for immediate success in this role, while also acknowledging any areas for improvement that could be addressed.

Evaluation Focus:

Technical Skills: Scrutinize the resume for evidence of proficiency in specific skills mentioned in the job description. Seek quantifiable achievements and tangible results that showcase exceptional mastery of each skill. Focus on recent and relevant experience directly applied to the required skills.
Experience: Analyze the candidate's experience section with a critical eye. Ensure clear descriptions of responsibilities and accomplishments directly related to the technical demands of the role. Verify that the described projects align with the job requirements and the skills claimed. Do not discount relevant volunteer work or personal projects if they showcase expertise.
Qualifications: Carefully examine the candidate's educational background and certifications, assessing whether they directly relate to the required technical expertise and exceed industry standards. Be open to alternative pathways and experiences that demonstrate equivalent competence (e.g., bootcamps, self-taught skills).
Communication and Presentation: Consider the clarity, conciseness, and professionalism of the resume's writing. Assess whether it effectively communicates the candidate's value proposition and aligns with the job description's tone and format.
Feedback Guidelines:

Provide targeted and actionable suggestions for addressing any identified weaknesses. Focus on recommendations that can be easily implemented in the candidate's resume or cover letter.
**Highlight potential areas where the candidate may be able to further strengthen their profile by showcasing exceptional achievements or unique qualifications.
Avoid generic feedback that is not specific to the candidate's profile or the job description.
Offer constructive criticism in a professional and encouraging manner.

try to give the output in concise format.
Here it is the  job description
description:{jd}
"""


## streamlit app
st.title("Score My Resume")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit1 = st.button("Percentage match")

submit3 = st.button("How Can I Improvise my Skills")


if submit1:
    if uploaded_file is not None:
        pdf_cotent=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt1)
        st.subheader(response)
    else:
        st.write("Please uplaod the resume")
       


if submit3:
    if uploaded_file is not None:
        pdf_cotent=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt3)
        st.subheader(response)
    else:
        st.write("Please uplaod the resume")