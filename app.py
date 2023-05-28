import streamlit as st
import openai
import os

openai.api_key = st.secrets["openai_api_key"]
st.set_page_config(page_title="Assisto", layout="centered")
st.markdown(""" <style>
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

patientData = {12344: {'name': 'John', 'age': '27', 'gender': 'Male', 'medical history': 'diabetes'}}

with st.container():
    st.title("Welcome to Assisto! :female-doctor:")
    st.header("Simplifying Your Health Journey, Assessing Symptoms and Suggesting Your Next Steps!")

st.divider()

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
    


with st.container():
    
    # with col1:
    #     print(None)
    #     st.subheader("Enter your prompt based on:")
    #     st.markdown(f"""
    #         1. Please describe your :red[primary symptoms] in detail, including any pain, discomfort, or abnormalities you are experiencing. \n
    #         2. Are there any :red[secondary symptoms or accompanying factors] that you have noticed? If so, please provide relevant information. \n
    #         3. Can you specify the :red[location, intensity, and duration] of your symptoms? Are there any triggers or relieving factors? \n
    #         4. Can you :red[provide details of previous occurrences and any treatments pursued]? Have you faced anything similar before? \n
    #         5. Do you have any :red[pre-existing medical conditions], allergies, or take any medications regularly? If so, please list them. \n
    #         6. Have there been any :red[recent lifestyle changes], such as changes in diet, exercise, or exposure to new environments? \n
    #         7. Have you had any :red[recent injuries, accidents, or surgeries]? \n
    #         8. Is there :red[any other relevant information] you would like to share? \n
    #     """)

    
    st.subheader("Tell me about your symptoms in detail :stethoscope: :")
    maintext = st.text_input("")
        
    with st.expander(":information_source:  Provide more informaiton below to help us diagnose you better:"):
        patientID = st.number_input("Patient ID", min_value=11111, max_value=99999, value=12345)
        name, age, gender = "-NA-", "-NA-", "-NA-"
        for i in patientData:
            if i == patientID:
                for j in patientData[i]:
                    if j == "medical history":
                        history = st.text_input("Can you :blue[provide details of previous occurrences or relevant medical history and any treatments pursued]? Have you faced anything similar before? (Pre-Filled)", value=patientData[i][j])
                    elif j == 'name':
                        name = patientData[i][j]
                    elif j == 'age':
                        age = patientData[i][j]
                    elif j == 'gender':
                        gender = patientData[i][j]
            else:
                history = st.text_input("Can you :blue[provide details of previous occurrences or relevant medical history and any treatments pursued]? Have you faced anything similar before?", key="hello")
                break
        if (name != None or name != "") and (age != None or age != "") and (gender != None or gender != ""):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("Name:  " + name)
            with col2:
                st.markdown("Age:  " + age)
            with col3:
                st.markdown("Gender:  " + gender)
        st.divider()
        symptoms = st.text_input("Describe your :blue[primary symptoms and secondary symptoms] in detail, including any pain, discomfort, or abnormalities you are experiencing.")
        location = st.text_input("Can you specify the :blue[location, intensity, and duration] of your symptoms? Are there any triggers or relieving factors?")
        recent = st.text_input("Have you had any :blue[recent injuries, accidents, or surgeries]?")
        additional = st.text_input("Is there :blue[any other relevant information] you would like to share?")

        compiledData = "Main Details: " + maintext + "\n Patient Symptoms: " + symptoms + "\n Location, Intensity and Duration of Symptoms " + location + "/n Previous Medical History of the Patient " + history + "Recent Lifestyle Changes, or injuries, accidents or surgeries the patient has gone through " + recent + "Any additional information: " + additional

    output = ""
    if (maintext != None and maintext != "") or (symptoms != None and symptoms != ""):
        prompt = f"""
        Based on the enclosed medical history provided within the triple backticks, please offer a reliable diagnosis considering all relevant factors. Explain the diagnosis in detail, including potential causes or conditions that align with the symptoms. Additionally, provide advice or recommendations for further evaluation, tests, or consultations. Remember, while this AI-based diagnosis aims to assist, it should not replace the expertise and judgment of a qualified healthcare professional. Encourage seeking professional medical advice for a definitive diagnosis and appropriate treatment. ```{compiledData}```
        """
        
        st.subheader("Your Diagnosis will appear below:")
        output = get_completion(prompt)
        
        with st.expander("Your Diagnosis:", expanded=True):
            st.markdown(output)

        PythonList = f"""
        Create a Python Dictionary with appropriate keys: Name, Age, Gender based on the data provided within the triple backticks, Symptoms, Diagnosis, suggested steps to be taken and severity of the case (between 1 to 10) based on the data provided within the triple exclamation marks. The symptom keywords and suggestion keywords must not exceed 3 words. The severity must be a number between 1 and 10.
        ```{compiledData}``` !!!{output}!!!
        """

        
        dictVal = get_completion(PythonList)
        #patientData.append(jsonResponse)
        st.subheader("JSON Output - To be fed to healthcare management system")
        st.code(dictVal)

        if isinstance(int(dictVal[-3]), int):
            if int(dictVal[-3]) >= 8:
                st.subheader(":red_circle: :red[You have an emergency condition, hospital has been intimated, visit immediately!]")
            elif int(dictVal[-3]) == 7:
                st.subheader(":warning: :yellow[You should visit the hospital as soon as possible] ")
            
    
    else:
        st.markdown(" ")

   
    

with st.container():
    if (maintext != None and maintext != "") or (symptoms != None and symptoms != ""):
        with st.expander("Diet Recommendation"):
            dietPlan = get_completion(f"""Consider the medical diagnosis in triple backticks to recommend a diet plan for the patient. Keep the diet recommendation in two parts, in the first part mention food items that should be avoided and in the second part mention food items that should be taken more of considering the diagnosis. 
            ```{output}```
            """)
            st.markdown(dietPlan)
        with st.expander("Simplified Diagnosis"):
            summary = get_completion(f"""
            Extract the diagnosis key specifically from {dictVal}. Explain the diagnosis you have extracted such that a child can understand. Do not exceed 80 words. Do not explain any other key from dictVal, especially the severity.
            """)
            st.markdown(summary)
            linktext = summary.replace(' ', '%20')
            url = f"""https://wa.me/?text={linktext}"""
            baseurl = "#"
        if output != None and output != "":
            st.markdown(f'''
            <a href="{baseurl}"><button style="background-color:#075E54; color:#fff">Share with WhatsApp</button></a>
            ''',
            unsafe_allow_html=True)
    
            