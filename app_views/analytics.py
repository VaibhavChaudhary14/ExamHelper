import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import data_manager as dm

def show():
    st.header("📊 Analytics Dashboard")
    
    # Get user_id from session state
    user_id = st.session_state.get("user_id")
    
    # Ensure user_id is not None
    if user_id is None:
        st.error("User ID is missing. Please log in.")
        return
    
    # Load study logs
    study_logs = dm.load_study_logs(user_id)

    if not study_logs.empty:
        # Convert timestamps
        study_logs['created_at'] = pd.to_datetime(study_logs['created_at'])
        
        # Summary metrics
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
        
        # Study time by subject
        st.subheader("Study Time Distribution")
        subject_time = study_logs.groupby('subject')['duration'].sum().reset_index()
        fig = px.pie(subject_time, values='duration', names='subject',
                     title='Time Spent per Subject (minutes)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Daily study time
        st.subheader("Daily Study Progress")
        daily_study = study_logs.groupby(study_logs['created_at'].dt.date)['duration'].sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_study.index, y=daily_study.values,
                                 mode='lines+markers', name='Minutes'))
        fig.update_layout(title='Daily Study Time',
                          xaxis_title='Date',
                          yaxis_title='Minutes')
        st.plotly_chart(fig, use_container_width=True)
        
        # Confidence level trends
        st.subheader("Confidence Level Trends")
        confidence_trend = study_logs.groupby('subject')['confidence_level'].mean().reset_index()
        fig = px.bar(confidence_trend, x='subject', y='confidence_level',
                     title='Average Confidence Level by Subject')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("Start logging your study sessions to see analytics!")
