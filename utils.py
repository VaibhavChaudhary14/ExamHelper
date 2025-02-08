from datetime import datetime, timedelta
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.study_assistant_db
habit_tracking = db.habit_tracking

def is_habit_completed(habit_id: str, user_id: str, date: datetime) -> bool:
    """Check if a habit was completed on a specific date"""
    record = habit_tracking.find_one({
        'habit_id': habit_id,
        'user_id': user_id,
        'date': date.date()
    })
    return record and record.get('completed', False)

def calculate_streak(habit_id: str, user_id: str) -> int:
    """Calculate current streak for a habit"""
    habit_data = list(habit_tracking.find({
        'habit_id': habit_id,
        'user_id': user_id,
        'completed': True
    }).sort('date', -1))  # Sort by date descending

    if not habit_data:
        return 0

    streak = 0
    today = datetime.now().date()
    current_date = today

    for record in habit_data:
        if record['date'] == current_date:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break

    return streak

def calculate_overall_completion_rate(user_id: str) -> float:
    """Calculate overall habit completion rate for a user"""
    total_tracked = habit_tracking.count_documents({'user_id': user_id})
    completed = habit_tracking.count_documents({'user_id': user_id, 'completed': True})

    return (completed / total_tracked) * 100 if total_tracked > 0 else 0.0

def format_duration(minutes: int) -> str:
    """Format duration in minutes to a human-readable string"""
    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours > 0:
        return f"{hours}h {remaining_minutes}m" if remaining_minutes > 0 else f"{hours}h"
    return f"{minutes}m"

def get_streak_emoji(streak: int) -> str:
    """Get appropriate emoji for streak length"""
    if streak >= 30:
        return "🔥"
    elif streak >= 7:
        return "⚡"
    elif streak > 0:
        return "✨"
    return "🌱"
