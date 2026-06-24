import streamlit as st
from langchain_groq import ChatGroq


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Health AI",
    layout="centered"
)


# ---------------- LOAD API KEY FROM STREAMLIT SECRETS ----------------
if "GROQ_API_KEY" not in st.secrets:
    st.error("GROQ_API_KEY not found in Streamlit Secrets")
    st.stop()


# ---------------- SESSION STATE ----------------
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "diet" not in st.session_state:
    st.session_state.diet = None


# ---------------- LOAD LLM ----------------
@st.cache_resource
def load_llm():

    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=1,
        api_key=st.secrets["GROQ_API_KEY"]
    )


llm = load_llm()


# ---------------- ANALYZE REPORT ----------------
def analyze_report(report, age, gender, activity, disease):

    prompt = f"""
You are a medical report analyzer.

Extract important numerical values and interpret them.

User details:
Age: {age}
Gender: {gender}
Activity level: {activity}
Diseases: {disease}

Medical Report:
{report}

Return:

- Extracted values
- Abnormal values
- Simple health summary

Keep the explanation easy to understand.
"""


    response = llm.invoke(prompt)

    return response.content



# ---------------- GENERATE DIET ----------------
def generate_diet(analysis):

    prompt = f"""
You are a professional diet planner.

Based on this medical analysis:

{analysis}


Create a structured diet plan:


Morning

Breakfast

Lunch

Evening snack

Dinner


Include:

- Foods to eat
- Foods to avoid
- Lifestyle tips


End with:

"Small steps today create a healthier tomorrow 💪"
"""


    response = llm.invoke(prompt)

    return response.content



# ---------------- UI ----------------

st.title("🩺 Health Report AI Analyzer")


tab1, tab2 = st.tabs(
    [
        "📄 Analysis",
        "🥗 Diet Plan"
    ]
)



# ---------------- TAB 1 ----------------

with tab1:


    report = st.text_area(
        "Medical Report Text"
    )


    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100
    )


    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female"
        ]
    )


    activity = st.selectbox(
        "Activity Level",
        [
            "Low",
            "Moderate",
            "High"
        ]
    )


    disease = st.text_area(
        "Diseases (if any)"
    )



    if st.button("Analyze Report"):


        if report.strip():


            with st.spinner("Analyzing report..."):


                result = analyze_report(
                    report,
                    age,
                    gender,
                    activity,
                    disease
                )


            st.session_state.analysis = result


            st.success(
                "Analysis Completed"
            )


            st.write(result)



        else:

            st.warning(
                "Please enter medical report"
            )




# ---------------- TAB 2 ----------------

with tab2:


    if st.session_state.analysis:


        if st.button("Generate Diet Plan"):


            with st.spinner("Creating diet plan..."):


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