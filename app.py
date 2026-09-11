
import streamlit as st
import pandas as pd
from groq import Groq


# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Sahaara AI",
    page_icon="🌸",
    layout="centered"
)


# -------------------------
# Groq Connection
# -------------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# -------------------------
# Load Opportunity Database
# -------------------------

@st.cache_data
def load_data():
    return pd.read_csv("opportunities.csv")


opportunities = load_data()


# -------------------------
# Title
# -------------------------

st.title("🌸 Sahaara AI")
st.subheader(
    "AI-powered pathway to skills, opportunities and financial independence"
)


st.write(
    "Tell us about yourself. Sahaara AI will suggest suitable pathways."
)


# -------------------------
# User Inputs
# -------------------------

city = st.text_input(
    "Your City",
    placeholder="e.g., Multan"
)

education = st.text_input(
    "Your Education",
    placeholder="e.g., Intermediate"
)

skills = st.text_input(
    "Your Current Skills",
    placeholder="e.g., Basic computer, typing"
)

goal = st.text_input(
    "Your Goal",
    placeholder="e.g., Work from home and start earning"
)


# -------------------------
# Matching Function
# -------------------------

def match_opportunities(city, education, skills):

    results = opportunities.copy()

    text = (
        city + " " +
        education + " " +
        skills
    ).lower()

    results["match_score"] = 0


    for index, row in results.iterrows():

        row_text = " ".join(
            row.astype(str)
        ).lower()


        score = 0

        for word in text.split():

            if word in row_text:
                score += 1


        results.loc[index, "match_score"] = score


    return results.sort_values(
        "match_score",
        ascending=False
    ).head(3)



# -------------------------
# Generate AI Response
# -------------------------

def generate_response(user_info, matched_data):

    prompt = f"""

You are Sahaara AI helping women in Pakistan.

User information:
{user_info}


Available verified opportunities:

{matched_data}


Give a short practical guidance.

Use this structure:

1. Aap ki situation

2. Suitable pathways

3. First step

4. Skills to develop

5. Sahaara note


Do not invent organizations, deadlines or fees.

"""


    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

       messages=[
    {
        "role": "system",
        "content": """
You are Sahaara AI, a supportive guidance assistant for women in Pakistan.

Follow these rules strictly:

- Use only verified opportunity information provided in the data.
- Do not invent organizations, registration links, deadlines, fees, or application procedures.
- Do not create numerical targets, benchmarks, or performance requirements.
- Do not mention typing speed, WPM, accuracy percentages, income estimates, or timelines unless explicitly available in verified data.
- Do not exaggerate the user's skills.
- Give simple, realistic guidance suitable for women with different education levels.

Use this structure:

1. Aap ki situation

2. Suitable pathways

3. First step

4. Skills to develop

5. Sahaara action pathway

6. Sahaara note
"""
    },
    {
        "role": "user",
        "content": prompt
    }
],

        temperature=0.3
    )


    return response.choices[0].message.content



# -------------------------
# Button
# -------------------------

if st.button("Get Sahaara Guidance"):

    if city and education and skills and goal:

        matched = match_opportunities(
            city,
            education,
            skills
        )


        user_info = f"""
City: {city}
Education: {education}
Skills: {skills}
Goal: {goal}
"""


        answer = generate_response(
            user_info,
            matched.to_string()
        )


        st.markdown(answer)


    else:

        st.warning(
            "Please complete all fields."
        )
