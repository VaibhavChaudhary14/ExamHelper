import streamlit as st
import data_manager as dm
import uuid
from datetime import datetime

def show():
    st.header("🎯 Personal Development")
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Set New Goal")
        
        with st.form("personal_goal"):
            title = st.text_input("Goal Title")
            description = st.text_area("Goal Description")
            category = st.selectbox(
                "Category",
                ["Academic", "Personal Growth", "Health", "Career"]
            )
            target_date = st.date_input("Target Date")
            
            if st.form_submit_button("Add Goal"):
                dm.add_personal_goal(
                    str(uuid.uuid4()),
                    title,
                    description,
                    category,
                    target_date
                )
                st.success("Goal added successfully!")
    
    with col2:
        st.subheader("Tips & Resources")
        with st.expander("Time Management"):
            st.write("""
            - Break large tasks into smaller ones
            - Use the Pomodoro Technique (25 min work, 5 min break)
            - Set specific goals for each study session
            - Regularly review and adjust your schedule
            """)
            
        with st.expander("Stay Motivated"):
            st.write("""
            - Celebrate small wins
            - Join study groups
            - Track your progress
            - Reward yourself after achieving goals
            """)
            
        with st.expander("Overcome Challenges"):
            st.write("""
            - Identify triggers for procrastination
            - Create a distraction-free study environment
            - Practice self-compassion
            - Seek support when needed
            """)
