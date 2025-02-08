import pandas as pd
from datetime import datetime
import uuid
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.study_assistant_db
habits = db.habits
habit_tracking = db.habit_tracking
study_logs = db.study_logs
personal_goals = db.personal_goals
progress_tracking = db.progress_tracking

def load_habits(user_id: str):
    """Load habits for a specific user"""
    data = list(habits.find({'user_id': user_id}))
    return pd.DataFrame(data) if data else pd.DataFrame()

def load_tracking(user_id: str):
    """Load tracking data for a specific user"""
    data = list(habit_tracking.find({'user_id': user_id}))
    if data:
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date']).dt.date
        return df
    return pd.DataFrame()

def add_habit(user_id: str, name: str, description: str, category: str):
    """Add a new habit for a user"""
    new_habit = {
        'habit_id': str(uuid.uuid4()),
        'user_id': user_id,
        'name': name,
        'description': description,
        'category': category,
        'created_at': datetime.now()
    }
    habits.insert_one(new_habit)

def track_habit(user_id: str, habit_id: str, date: datetime, completed: bool):
    """Track a habit's completion status"""
    tracking_data = {
        'user_id': user_id,
        'habit_id': habit_id,
        'date': date.date(),
        'completed': completed,
        'updated_at': datetime.now()
    }
    habit_tracking.update_one(
        {'user_id': user_id, 'habit_id': habit_id, 'date': date.date()},
        {'$set': tracking_data},
        upsert=True
    )

def load_study_logs(user_id: str):
    """Load study logs for a specific user"""
    data = list(study_logs.find({'user_id': user_id}))
    return pd.DataFrame(data) if data else pd.DataFrame()

def add_study_log(user_id: str, subject: str, topic: str, duration: int, confidence_level: int, notes: str):
    """Add a new study log"""
    new_log = {
        'log_id': str(uuid.uuid4()),
        'user_id': user_id,
        'subject': subject,
        'topic': topic,
        'duration': duration,
        'confidence_level': confidence_level,
        'notes': notes,
        'created_at': datetime.now()
    }
    study_logs.insert_one(new_log)

def load_personal_goals(user_id: str):
    """Load personal goals for a specific user"""
    data = list(personal_goals.find({'user_id': user_id}))
    return pd.DataFrame(data) if data else pd.DataFrame()

def add_personal_goal(user_id: str, title: str, description: str, category: str, target_date: datetime):
    """Add a new personal goal"""
    new_goal = {
        'goal_id': str(uuid.uuid4()),
        'user_id': user_id,
        'title': title,
        'description': description,
        'category': category,
        'target_date': target_date,
        'completed': False,
        'created_at': datetime.now()
    }
    personal_goals.insert_one(new_goal)

def update_goal_status(user_id: str, goal_id: str, completed: bool):
    """Update the completion status of a goal"""
    personal_goals.update_one(
        {'user_id': user_id, 'goal_id': goal_id},
        {'$set': {'completed': completed, 'updated_at': datetime.now()}}
    )
