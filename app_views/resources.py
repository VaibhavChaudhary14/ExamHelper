import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import data_manager as dm

def show():
    st.header("📚 Support Resources")
    
    tab1, tab2, tab3 = st.tabs(["Study Resources", "Health & Wellness", "Professional Help"])
    
    with tab1:
        st.subheader("Study Materials")
        
        st.write("##### GATE Exam Resources")
        st.markdown("""
        - [Official GATE Website](https://gate.iitk.ac.in/)
        - [Previous Year Papers](https://gate.iitk.ac.in/previous-question-papers)
        - [Syllabus and Exam Pattern](https://gate.iitk.ac.in/syllabus)
        - [Video Lectures on NPTEL](https://nptel.ac.in/)
        """)
        
        st.write("##### CAT Exam Resources")
        st.markdown("""
        - [Official CAT Website](https://iimcat.ac.in/)
        - [Sample Questions](https://iimcat.ac.in/mock-test)
        - [Preparation Tips](https://iimcat.ac.in/per/g01/pub/756/preparationtips/)
        """)
        
        # Analytics Dashboard for CAT Exam Preparation
        st.subheader("📊 Analytics Dashboard")
        
        user_id = st.session_state.get("user_id")
        study_logs = dm.load_study_logs(user_id)
        
        if not study_logs.empty:
            study_logs['created_at'] = pd.to_datetime(study_logs['created_at'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_hours = study_logs['duration'].sum() / 60
                st.metric("Total Study Hours", f"{total_hours:.1f}")
            
            with col2:
                avg_confidence = study_logs['confidence_level'].mean()
                st.metric("Average Confidence", f"{avg_confidence:.1f}/5")
            
            with col3:
                subjects_covered = len(study_logs['subject'].unique())
                st.metric("Subjects Covered", subjects_covered)
            
            st.subheader("Study Time Distribution")
            subject_time = study_logs.groupby('subject')['duration'].sum().reset_index()
            fig = px.pie(subject_time, values='duration', names='subject', title='Time Spent per Subject (minutes)')
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Daily Study Progress")
            daily_study = study_logs.groupby(study_logs['created_at'].dt.date)['duration'].sum()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_study.index, y=daily_study.values, mode='lines+markers', name='Minutes'))
            fig.update_layout(title='Daily Study Time', xaxis_title='Date', yaxis_title='Minutes')
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Confidence Level Trends")
            confidence_trend = study_logs.groupby('subject')['confidence_level'].mean().reset_index()
            fig = px.bar(confidence_trend, x='subject', y='confidence_level', title='Average Confidence Level by Subject')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Start logging your study sessions to see analytics!")
    
    with tab2:
        st.subheader("Health & Wellness")
        
        with st.expander("Stress Management"):
            st.markdown("""
            - Practice deep breathing exercises
            - Take regular breaks during study sessions
            - Maintain a balanced diet and exercise routine
            - Get adequate sleep (7-8 hours daily)
            - Practice mindfulness and meditation
            """)
        
        with st.expander("Digital Wellness"):
            st.markdown("""
            - Use website blockers during study time
            - Set screen time limits
            - Take regular breaks from devices
            - Use blue light filters in evening hours
            - Practice digital detox on weekends
            """)
        
        with st.expander("Physical Health"):
            st.markdown("""
            - Exercise for at least 30 minutes daily
            - Maintain good posture while studying
            - Take regular eye breaks (20-20-20 rule)
            - Stay hydrated
            - Eat balanced, nutritious meals
            """)
    
    with tab3:
        st.subheader("Professional Support")
        
        st.info("If you're struggling with addiction or mental health challenges, professional help is available and confidential.")
        
        st.markdown("""
        ##### Helpline Numbers
        - National Mental Health Helpline: 1800-599-0019
        - Student Counselling Services: [Available at your institution]
        
        ##### Online Counselling Resources
        - Professional online counseling platforms
        - Support groups and communities
        - Institution counseling services
        
        Remember, seeking help is a sign of strength, not weakness.
        """)
        
        st.write("##### Additional Resources")
        st.markdown("""
        - [WHO Mental Health Resources](https://www.who.int/mental_health/)
        - [Mental Health Foundation](https://www.mentalhealth.org.uk/)
        - [Addiction Support Resources](https://www.samhsa.gov/)
        """)
