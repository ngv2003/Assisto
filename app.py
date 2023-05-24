import streamlit as st
import openai
import os

openai.api_key = st.secrets["openai_api_key"]
st.set_page_config(layout="wide")


with st.container():
    st.title("Welcome to Assisto!")
    st.header("An application that uses **generative AI** to help doctors make fast and accurate diagnosis")

st.divider()

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

patientData = []


with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Enter your prompt based on:")
        st.markdown(f"""
            1. Please describe your :red[primary symptoms] in detail, including any pain, discomfort, or abnormalities you are experiencing. \n
            2. Are there any :red[secondary symptoms or accompanying factors] that you have noticed? If so, please provide relevant information. \n
            3. Can you specify the :red[location, intensity, and duration] of your symptoms? Are there any triggers or relieving factors? \n
            4. Have you experienced similar symptoms in the past? If yes, please :red[provide details of previous occurrences and any treatments pursued]. \n
            5. Do you have any :red[pre-existing medical conditions], allergies, or take any medications regularly? If so, please list them. \n
            6. Have there been any :red[recent lifestyle changes], such as changes in diet, exercise, or exposure to new environments? \n
            7. Have you had any :red[recent injuries, accidents, or surgeries]? \n
            8. Is there :red[any other relevant information] you would like to share? \n
        """)

    with col2:
        st.subheader("Enter issue:")
        text = st.text_area("", height = 60)

    if text != None and text != "":
        prompt = f"""
        Given the provided symptoms and medical history enclosed within the triple backticks, please provide a comprehensive and data-driven diagnosis for the patient. Consider all relevant factors, such as the reported symptoms, duration, severity, associated conditions, and any additional information provided. Please ensure the diagnosis is accurate, reliable, and backed by medical expertise. Provide a detailed explanation of the diagnosis, including potential causes or conditions that could explain the symptoms. Include any relevant advice or recommendations for further evaluation, tests, or consultations. Remember, while this AI-based diagnosis is meant to assist, it should not replace the expertise and judgment of a qualified healthcare professional. Encourage seeking professional medical advice for a definitive diagnosis and appropriate treatment.
        ```{text}```
        """
        with col2:
            st.markdown("Diagnosis: (Please wait for 20-30 seconds)")
            output = get_completion(prompt)
            st.markdown(output)

        jsonFile = f"""
        Create a JSON File with appropriate keys: Name, Age, Gender based on the data provided within the triple backticks, Symptoms, suggested steps to be taken and severity of the case (out of 10) based on the data provided within the triple exclamation marks. The symptom keywords and suggestion keywords must not exceed 3 words. The severity must be a number between 1 and 10.
        ```{text}``` !!!{output}!!!
        """

        with col2:
            jsonResponse = get_completion(jsonFile)
            patientData.append(jsonResponse)
            st.code(jsonResponse)
    else:
        with col2:
            st.markdown("Please input your issue based on the format: **Name Age Gender and Relevant Information**")