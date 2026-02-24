import streamlit as st
from huggingface_hub import InferenceClient
import os

# --- 1. MODEL & PROMPT LOGIC ---

def query_model(prompt):
    try:
        HF_TOKEN = os.getenv("HF_TOKEN")
        
        client = InferenceClient(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            token=HF_TOKEN
        )

        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a certified professional fitness trainer. Output only the workout plan without conversational filler."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to AI: {str(e)}"

def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)

def bmi_category(bmi):
    if bmi < 18.5: return "Underweight"
    elif bmi < 25: return "Normal Weight"
    elif bmi < 30: return "Overweight"
    else: return "Obese"

# Added 'age' parameter here
def build_prompt(name, age, gender, height, weight, goal, fitness_level, equipment):
    bmi = calculate_bmi(weight, height)
    bmi_status = bmi_category(bmi)
    equipment_list = ", ".join(equipment) if equipment else "No Equipment"

    # Added 'Age' to the prompt text
    prompt = f"""
Create a structured 5-day personalized workout plan for {name}.
User Profile:
- Age: {age}
- Gender: {gender} | BMI: {bmi:.2f} ({bmi_status})
- Goal: {goal} | Level: {fitness_level}
- Available Equipment: {equipment_list}

Instructions:
1. Divide clearly into Day 1, Day 2, Day 3, Day 4, and Day 5.
2. For each day, list 4-6 exercises with: Name, Sets/Reps, and Rest Time.
3. Adjust intensity for {fitness_level} level, age {age}, and {bmi_status} status.
4. Output the plan in a clean, professional list format.
"""
    return prompt, bmi, bmi_status

# --- 2. FRONTEND CONFIG ---

st.set_page_config(page_title="FitPlan AI 💪", page_icon="💪", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; }
    .main-title { color: #00ffcc; text-align: center; font-size: 3rem; font-weight: bold; margin-top: -50px; }
    div.stButton > button:first-child {
        background: #00ffcc; color: black; font-weight: bold; width: 100%; border-radius: 50px; height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'login'

# --- PAGE 1: PROFILE FORM ---
if st.session_state.page == 'login':
    st.markdown('<h1 class="main-title">FitPlan AI 💪</h1>', unsafe_allow_html=True)
    st.write("### User Profile & Health Metrics")

    name = st.text_input("Name (Required)")
    
    # Added Age input field
    col_age, col_gen = st.columns(2)
    with col_age:
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
    with col_gen:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
    col1, col2 = st.columns(2)
    with col1:
        height_cm = st.number_input("Height (cm)", min_value=0.0, step=0.1)
    with col2:
        weight_kg = st.number_input("Weight (kg)", min_value=0.0, step=0.1)

    goal = st.selectbox("Fitness Goal", ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexible"])
    level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
    
    equipment = st.multiselect("Available Equipment", [
        "Dumbbells", "Resistance band", "Yoga mat", "No equipment", "Inclined bench", 
        "Treadmill", "Cycle", "Skipping rope", "Hand gripper", "Pullups bar", 
        "Weight plates", "Hula hoop ring", "Bosu ball"
    ])

    if st.button("🚀 GENERATE MY WORKOUT PLAN"):
        if not name or height_cm <= 0 or weight_kg <= 0 or not equipment:
            st.error("Please fill in all fields and select equipment.")
        else:
            with st.spinner("AI Trainer is crafting your plan..."):
                # 1. Build the prompt (passed 'age' here)
                prompt_text, bmi, bmi_status = build_prompt(name, age, gender, height_cm, weight_kg, goal, level, equipment)
                
                # 2. Query the Mistral Model
                workout_plan = query_model(prompt_text)
                
                # 3. Save to session state
                st.session_state.user_data = {
                    "name": name, "age": age, "bmi": round(bmi, 2), "category": bmi_status, 
                    "goal": goal, "level": level, "equipment": equipment,
                    "plan": workout_plan
                }
                st.session_state.page = 'generator'
                st.rerun()

# --- PAGE 2: ANALYSIS & RECOMMENDATION ---
elif st.session_state.page == 'generator':
    u = st.session_state.user_data
    st.markdown(f"<h1 class='main-title'>Analysis for {u['name']}</h1>", unsafe_allow_html=True)
    
    # Added Age to the display summary
    st.success(f"**Age:** {u['age']} | **BMI:** {u['bmi']} ({u['category']}) | **Goal:** {u['goal']}")
    
    st.subheader("🏋️ Personalized 5-Day Workout Plan")
    
    st.markdown(u['plan'])

    if st.button("⬅️ Edit Profile"):
        st.session_state.page = 'login'
        st.rerun()
