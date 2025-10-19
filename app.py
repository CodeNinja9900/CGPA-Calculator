import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="GPA & CGPA Calculator", layout="wide")

# Define the grading system
grade_points = {
    'A': 4.00,
    'A-': 3.67,
    'B+': 3.33,
    'B': 3.00,
    'B-': 2.67,
    'C+': 2.33,
    'C': 2.00,
    'C-': 1.67,
    'D+': 1.33,
    'D': 1.00,
    'F': 0.00
}

def calculate_gpa(grades, credit_hours):
    if len(grades) != len(credit_hours):
        return 0.0
    
    total_points = sum(grade_points[grade] * credit for grade, credit in zip(grades, credit_hours))
    total_credits = sum(credit_hours)
    
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

# Main app
st.title("🎓 GPA & CGPA Calculator")
st.markdown("---")

# Sidebar for CGPA calculation
with st.sidebar:
    st.header("Calculate CGPA")
    num_semesters = st.number_input("Number of Semesters", min_value=1, max_value=12, value=1)
    
    semester_gpas = []
    semester_credits = []
    
    for i in range(num_semesters):
        st.subheader(f"Semester {i+1}")
        gpa = st.number_input(f"GPA", key=f"gpa_{i}", min_value=0.0, max_value=4.0, value=0.0, step=0.01)
        credits = st.number_input(f"Credit Hours", key=f"credits_{i}", min_value=0, max_value=24, value=15)
        semester_gpas.append(gpa)
        semester_credits.append(credits)
    
    if st.button("Calculate CGPA"):
        total_points = sum(gpa * credits for gpa, credits in zip(semester_gpas, semester_credits))
        total_credits = sum(semester_credits)
        cgpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
        st.success(f"Your CGPA is: {cgpa}")

# Main content for GPA calculation
st.header("Calculate Semester GPA")
num_subjects = st.number_input("Number of Subjects", min_value=1, max_value=8, value=5)

# Create columns for input
grades = []
credits = []

for i in range(num_subjects):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"Subject {i+1}")
    with col2:
        grade = st.selectbox(
            f"Grade for Subject {i+1}",
            options=list(grade_points.keys()),
            key=f"grade_{i}"
        )
        grades.append(grade)
    with col3:
        credit = st.number_input(
            f"Credit Hours for Subject {i+1}",
            min_value=1,
            max_value=4,
            value=3,
            key=f"credit_{i}"
        )
        credits.append(credit)

if st.button("Calculate GPA"):
    gpa = calculate_gpa(grades, credits)
    st.success(f"Your GPA is: {gpa}")
    
    # Display grade points table
    st.markdown("---")
    st.subheader("Grade Points Reference Table")
    
    grade_data = {
        'Grade': list(grade_points.keys()),
        'Grade Points': list(grade_points.values()),
        'Percentage Equivalent': [
            '90-100%', '85-89%', '80-84%', '75-79%', '70-74%',
            '65-69%', '60-64%', '55-59%', '50-54%', '45-49%', 'Below 45%'
        ]
    }
    
    df = pd.DataFrame(grade_data)
    st.table(df)