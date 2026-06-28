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
You are an expert Medical Report Analysis Assistant capable of analyzing medical data from:
- Text reports
- Images (scanned reports, photos of prescriptions, lab reports)
- PDF documents
- Word documents
- Any structured or unstructured medical report format

Your job is to extract, interpret, and summarize medical information in simple language.

IMPORTANT RULE:
If the input is NOT related to a medical/health report, respond only with:
"Invalid input: Please provide a valid medical report (image, PDF, or document) for analysis."
and stop immediately.

-------------------------
INPUT DATA
-------------------------
Disease/Condition (if provided): {disease}
Patient Activity (if provided): {activity}
Weight (if provided): {weight}
Medical Report (text/image/pdf/doc): {file}

-------------------------
TASKS
-------------------------

1. Extracted Values:
- Extract all medical parameters, lab results, observations, or measurements.
- Include units (mg/dL, mmol/L, %, mmHg, etc.).
- Works even if data comes from images or scanned documents.

2. Abnormal Values:
- Identify values outside normal medical reference ranges.
- Mark each as HIGH, LOW, or NORMAL borderline.
- If reference range is missing, use standard clinical reference values.

3. Simple Health Summary:
- Provide an easy-to-understand explanation of overall health condition.
- Highlight possible risks or concerns if abnormal values exist.
- Do NOT give a final diagnosis.
- Keep language simple for non-medical users.

-------------------------
OUTPUT FORMAT
-------------------------

Extracted Values:
- ...

Abnormal Values:
- ...

Simple Health Summary:
- ...
"""


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