import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os
a=os.getenv("groq_api_key")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Health AI",
    layout="centered"
)




api_key = a


# ---------------- INIT SESSION STATE ----------------
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "diet" not in st.session_state:
    st.session_state.diet = None


# ---------------- LOAD LLM (CACHED) ----------------
@st.cache_resource
def load_llm():

    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=1,
        api_key=api_key
    )


llm = load_llm()


# ---------------- FUNCTION 1 ----------------
def analyze_report(file,weight,activity,disease):

    prompt = f"""

You are a medical report analyzer.

Extract important numerical values and interpret them.


Diseases: {disease}

Activity: {activity}

Weight: {weight}

Use this for Medical Report: {file}


Return:

- Extracted values
- Abnormal values
- Simple health summary


If the input is not realated to medical report or the input is not a general form give the warning corresponding to the needed input and stop prcoeeding.then 
ask for the appropriate input.

"""


    response = llm.invoke(prompt)

    return response.content



# ---------------- FUNCTION 2 ----------------
def generate_diet(analysis):

    prompt = f"""

You are a professional diet planner.

Based on this medical analysis:

{analysis}


Create a structured diet plan if it has a proper input:

Morning
Breakfast
Lunch
Evening snack
Dinner


Include:

- Foods to eat
- Foods to avoid
- Lifestyle tips

If the diet plan is successfully generated 
End with:

"Small steps today create a healthier tomorrow 💪"

Else warning about the incomplete analyis due to incomplete input. 

"""


    response = llm.invoke(prompt)

    return response.content



# ---------------- STREAMLIT UI ----------------

st.title("🩺 Health Report AI Analyzer")


tab1, tab2 = st.tabs(
    ["📄 Analysis", "🥗 Diet Plan"]
)



# ---------------- TAB 1 ----------------

with tab1:

    

    file = st.file_uploader("Upload img")

   
    activity = st.selectbox(
        "Activity Level",
        ["Low", "Moderate", "High"]
    )


    disease = st.text_area(
        "Diseases (if any)"
    )
    
    weight=st.number_input(
        "Weight in kg",
         min_value=0,
         max_value=160
    )


    if st.button("Analyze Report"):


        if file:


            with st.spinner(
                "Analyzing report..."
            ):


                result = analyze_report(
                    file,
                    weight,
                    activity,
                    disease
                )


            st.session_state.analysis = result


            st.success(
                "Analysis Completed"
            )


            st.write(result)


        



# ---------------- TAB 2 ----------------

with tab2:


    if st.session_state.analysis:


        if st.button("Generate Diet Plan"):


            with st.spinner(
                "Creating diet plan..."
            ):


                diet = generate_diet(
                    st.session_state.analysis
                )


            st.session_state.diet = diet


            st.success(
                "Diet Plan Ready 🎯"
            )


            st.write(diet)


            st.markdown(
                "🌟 Stay consistent — small steps lead to big health improvements!"
            )


    else:

        st.info(
            "Please complete analysis first"
        )