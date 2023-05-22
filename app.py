import streamlit as st
import openai
import os

openai.api_key = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

patientData = []


st.title("Welcome to Assisto")
st.markdown("An application that uses **generative AI** to help doctors make fast and accurate diagnosis")
st.markdown("Please state your problem as: <Name> <Age> <Gender> : <Issue>")
text = st.text_input("Enter Prompt")

if text != None and text != "":
    prompt = f"""
    You are an assistant medical diagnosing agent. You take in medical symptoms input that has been provided within triple backticks. You must give suggestions as to any best practices, or tests to be taken, or a predictive diagnosis based on the symptoms. If you're unsure, do not suggest false information, simply say - Doctor's diagnosis required.
    If the prompt provided is not medical based, then simply say: Hi I am Assisto and I am a Medical Assistant, please provide medical details on your issue.
    If all the data (Name, Age, Gender, Symptoms) isn't provided, then please display: All data not provided, please reinput issue.
    ```{text}```
    """

    st.markdown("Diagnosis:")
    st.markdown(get_completion(prompt))

    jsonFile = f"""
    Create a JSON File with appropriate keys: Name, Age, Gender and Symptoms based on the data provided within the triple backticks. The symptom keywords must not exceed 3 words.
    ```{text}```
    """
    jsonResponse = get_completion(jsonFile)

    patientData.append(jsonResponse)
    st.markdown(jsonResponse)
else:
    st.markdown("Please input your issue based on the format")