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
You are an expert Medical Report Analysis Assistant.

Your job is to carefully analyze ANY medical report provided (blood tests, urine tests, imaging reports, pathology reports, diagnostic summaries, etc.) and extract meaningful insights in simple language.

You must ONLY proceed if the input is a valid medical report. If the input is unrelated to medical/health reports, respond with a warning:
"Invalid input: Please provide a valid medical report for analysis."
and stop further processing.

-------------------------
INPUT DATA
-------------------------
Disease/Condition (if given): {disease}
Patient Activity (if given): {activity}
Weight (if given): {weight}
Medical Report Document/image: {file}

-------------------------
TASKS
-------------------------

1. Extracted Values:
- Identify all important medical values, lab results, measurements, or observations from the report.
- Include units (e.g., mg/dL, mmHg, %, etc.).
- Present them in a clean list format.

2. Abnormal Values:
- Detect values that are outside the normal reference range.
- Clearly mention whether each is HIGH or LOW.
- If reference ranges are not provided, infer standard clinical ranges when possible.

3. Simple Health Summary:
- Explain the overall health condition in simple, non-technical language.
- Mention possible concerns if abnormal values exist.
- Keep it easy for a non-medical person to understand.
- Avoid diagnosis claims; focus on interpretation and insight.

-------------------------
OUTPUT FORMAT
-------------------------

Extracted Values:
- ...

Abnormal Values:
- ...

Simple Health Summary:"""

   response = llm.invoke(prompt)

   return response.content



# ---------------- FUNCTION 2 ----------------
def generate_diet(analysis):

    prompt = f"""

You are a professional diet planner.

Based on this medical analysis:

{analysis}


Create a structured diet plan only if it strictly has all values for medical analysis.Don't create hypothetical diet plan.
For:
Morning
Breakfast
Lunch
Evening snack
Dinner


Include:

- Foods to eat
- Foods to avoid
- Lifestyle tips

If the diet plan is successfully generated for the medical analysis
End with:

Displays :
"Small steps today create a healthier tomorrow 💪" this only when the healthy diet is generated.

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