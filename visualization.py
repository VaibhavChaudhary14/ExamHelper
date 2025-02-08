import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

def plot_completion_rates():
    """Create a bar chart showing completion rates for each habit"""
    habits_df = pd.read_csv('habits.csv')
    tracking_df = pd.read_csv('tracking.csv')
    
    completion_rates = []
    for _, habit in habits_df.iterrows():
        habit_tracking = tracking_df[tracking_df['habit_id'] == habit['habit_id']]
        if not habit_tracking.empty:
            completion_rate = (
                len(habit_tracking[habit_tracking['completed'] == True]) / 
                len(habit_tracking) * 100
            )
        else:
            completion_rate = 0
        completion_rates.append({
            'habit': habit['name'],
            'completion_rate': completion_rate
        })
    
    df = pd.DataFrame(completion_rates)
    fig = px.bar(
        df,
        x='habit',
        y='completion_rate',
        title='Habit Completion Rates (%)',
        labels={'habit': 'Habit', 'completion_rate': 'Completion Rate (%)'}
    )
    return fig

def plot_weekly_progress():
    """Create a line chart showing weekly progress"""
    tracking_df = pd.read_csv('tracking.csv')
    tracking_df['date'] = pd.to_datetime(tracking_df['date'])
    
    # Get last 7 days
    last_7_days = pd.date_range(
        end=datetime.now(),
        periods=7,
        freq='D'
    )
    
    daily_completion = tracking_df[tracking_df['date'].dt.date.isin(last_7_days.date)]
    daily_stats = daily_completion.groupby(
        tracking_df['date'].dt.date
    )['completed'].mean() * 100
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_stats.index,
        y=daily_stats.values,
        mode='lines+markers',
        name='Completion Rate'
    ))
    
    fig.update_layout(
        title='Weekly Progress',
        xaxis_title='Date',
        yaxis_title='Completion Rate (%)',
        showlegend=False
    )
    return fig

def plot_calendar_heatmap(habit_name):
    """Create a calendar heatmap for a specific habit"""
    habits_df = pd.read_csv('habits.csv')
    tracking_df = pd.read_csv('tracking.csv')
    
    habit_id = habits_df[habits_df['name'] == habit_name]['habit_id'].iloc[0]
    habit_tracking = tracking_df[tracking_df['habit_id'] == habit_id]
    
    # Create date range for the last 30 days
    date_range = pd.date_range(
        end=datetime.now(),
        periods=30,
        freq='D'
    )
    
    # Prepare data for heatmap
    habit_tracking['date'] = pd.to_datetime(habit_tracking['date'])
    tracking_dict = dict(zip(
        habit_tracking['date'].dt.date,
        habit_tracking['completed']
    ))
    
    z_values = [[int(tracking_dict.get(date.date(), 0)) for date in date_range]]
    
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=date_range,
        colorscale=[[0, 'lightgray'], [1, 'green']],
        showscale=False
    ))
    
    fig.update_layout(
        title=f'Calendar Heatmap - {habit_name}',
        height=200,
        xaxis_title='Date',
        yaxis_visible=False
    )
    return fig
