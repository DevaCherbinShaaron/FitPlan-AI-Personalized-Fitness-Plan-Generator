import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="FitPlan AI 💪", page_icon="💪", layout="wide")

# --- CUSTOM CSS (Fixed to remove empty top box) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; }
    .main-title { color: #00ffcc; text-align: center; font-size: 3rem; font-weight: bold; margin-top: -50px; }
    div.stButton > button:first-child {
        background: #00ffcc; color: black; font-weight: bold; width: 100%; border-radius: 50px; height: 3em;
    }
    /* Simple styling for the form area without creating an extra box container */
    [data-testid="stVerticalBlock"] > div:contains("Milestone 1") {
        background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px;
        border: 1px solid rgba(0, 255, 204, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'login'

# --- PAGE 1: PROFILE FORM ---
if st.session_state.page == 'login':
    # Removed the <div class="main-box"> that was causing the empty header
    st.markdown('<h1 class="main-title">FitPlan AI 💪</h1>', unsafe_allow_html=True)
    st.write("### User Profile & Health Metrics")

    # 1. Personal Information
    name = st.text_input("Name (Required)")
    col1, col2 = st.columns(2)
    with col1:
        height_cm = st.number_input("Height in centimeters (Required)", min_value=0.0, step=0.1)
    with col2:
        weight_kg = st.number_input("Weight in kilograms (Required)", min_value=0.0, step=0.1)

    # 2. Fitness Details
    goal = st.selectbox("Fitness Goal", ["Build Muscle", "Weight Loss", "Strength Gain", "Abs Building", "Flexible"])
    level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])
    
    equipment = st.multiselect("Available Equipment", [
        "Dumbbells", "Resistance band", "Yoga mat", "No equipment", "Inclined bench", 
        "Treadmill", "Cycle", "Skipping rope", "Hand gripper", "Pullups bar", 
        "Weight plates", "Hula hoop ring", "Bosu ball"
    ])

    if st.button("CALCULATE & SUBMIT"):
        # 5. Input Validation
        if not name or height_cm <= 0 or weight_kg <= 0:
            st.error("Please provide a valid name and positive values for height/weight.")
        else:
            # 3. BMI Logic
            height_m = height_cm / 100
            bmi = round(weight_kg / (height_m**2), 2)
            
            if bmi < 18.5: category = "Underweight"
            elif 18.5 <= bmi < 24.9: category = "Normal"
            elif 25.0 <= bmi < 29.9: category = "Overweight"
            else: category = "Obese"

            st.session_state.user_data = {
                "name": name, "bmi": bmi, "category": category, 
                "goal": goal, "level": level, "equipment": equipment
            }
            st.session_state.page = 'generator'
            st.rerun()

# --- PAGE 2: ANALYSIS & RECOMMENDATION ---
elif st.session_state.page == 'generator':
    u = st.session_state.user_data
    st.markdown(f"<h1 class='main-title'>Analysis for {u['name']}</h1>", unsafe_allow_html=True)
    st.success(f"**Your BMI:** {u['bmi']} | **Category:** {u['category']}")
    st.info(f"Goal: {u['goal']} | Level: {u['level']}")
    
    st.subheader("Personalized Fitness Recommendations")
    
    if "No equipment" in u['equipment'] or not u['equipment']:
        st.write("✅ **Recommendation:** Focus on Bodyweight Calisthenics (Pushups, Squats, Planks).")
    else:
        st.write(f"✅ **Recommendation:** Utilize your {', '.join(u['equipment'])} for compound movements.")

    reps = {"Beginner": "3 sets of 10", "Intermediate": "4 sets of 12", "Advanced": "5 sets of 15"}
    st.warning(f"As a **{u['level']}**, your target intensity is **{reps[u['level']]}**.")

    if st.button("⬅️ Edit Profile"):
        st.session_state.page = 'login'; st.rerun()
