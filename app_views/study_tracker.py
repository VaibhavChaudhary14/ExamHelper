import streamlit as st
import pandas as pd
from datetime import datetime
import data_manager as dm
import uuid

def show():
    st.header("📚 Study Tracker")
    
    # Create two columns for the layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Log Study Session")
        
        with st.form("study_log"):
            subject = st.selectbox(
                "Subject",
                ["GATE - Engineering Mathematics", "GATE - Computer Science", 
                 "CAT - Quantitative Aptitude", "CAT - Verbal Ability",
                 "CAT - Data Interpretation", "CAT - Logical Reasoning"]
            )
            
            topic = st.text_input("Topic Covered")
            
            duration = st.number_input(
                "Duration (minutes)",
                min_value=5,
                max_value=480,
                value=30,
                step=5
            )
            
            confidence = st.slider(
                "Confidence Level",
                min_value=1,
                max_value=5,
                value=3,
                help="1: Need more practice, 5: Fully confident"
            )
            
            notes = st.text_area("Study Notes")
            
            if st.form_submit_button("Save Study Log"):
                dm.add_study_log(
                    str(uuid.uuid4()),
                    subject,
                    topic,
                    duration,
                    confidence,
                    notes
                )
                st.success("Study session logged successfully!")
                st.session_state.study_logs = dm.load_study_logs()
    
    with col2:
        st.subheader("Recent Activity")
        if not st.session_state.study_logs.empty:
            for _, log in st.session_state.study_logs.head(5).iterrows():
                with st.expander(f"{log['subject']} - {log['topic']}", expanded=False):
                    st.write(f"Duration: {log['duration']} minutes")
                    st.write(f"Confidence: {'⭐' * log['confidence_level']}")
                    if log['notes']:
                        st.write("Notes:", log['notes'])
        else:
            st.info("No study sessions logged yet. Start tracking your study time!")
