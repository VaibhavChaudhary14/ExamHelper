import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment, default to local instance
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')

try:
    # Create MongoDB client
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)

    # Test the connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB")

    db = client.study_assistant_db

    # Collection definitions (equivalent to tables in SQL)
    users = db.users
    habits = db.habits
    habit_tracking = db.habit_tracking
    study_logs = db.study_logs
    personal_goals = db.personal_goals
    progress_tracking = db.progress_tracking

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    # Create dummy collections for development/testing
    class DummyCollection:
        def __init__(self):
            self.data = []

        def find(self, *args, **kwargs):
            return []

        def find_one(self, *args, **kwargs):
            return None

        def insert_one(self, *args, **kwargs):
            self.data.append(args[0] if args else kwargs.get('document', {}))
            return type('InsertOneResult', (), {'inserted_id': len(self.data)})

        def update_one(self, *args, **kwargs):
            return type('UpdateResult', (), {'modified_count': 0, 'matched_count': 0})

        def create_index(self, *args, **kwargs):
            pass

        def command(self, *args, **kwargs):
            return {"ok": 1.0}

    users = DummyCollection()
    habits = DummyCollection()
    habit_tracking = DummyCollection()
    study_logs = DummyCollection()
    personal_goals = DummyCollection()
    progress_tracking = DummyCollection()

def init_db():
    """
    Initialize database indexes
    """
    try:
        # Create indexes for better query performance
        users.create_index('email', unique=True)
        users.create_index('username', unique=True)
        habits.create_index([('user_id', 1), ('habit_id', 1)], unique=True)
        habit_tracking.create_index([('habit_id', 1), ('date', 1)])
        study_logs.create_index([('user_id', 1), ('created_at', -1)])
        personal_goals.create_index([('user_id', 1), ('goal_id', 1)], unique=True)
        progress_tracking.create_index('tracking_id', unique=True)
        print("Database indexes created successfully")
    except Exception as e:
        print(f"Error creating indexes: {e}")

# Initialize database indexes
init_db()

# Document schemas (for reference - MongoDB is schema-less)
USER_SCHEMA = {
    'user_id': str,  # UUID string
    'username': str,
    'email': str,
    'password_hash': bytes,
    'created_at': datetime,
    'last_login': datetime
}

HABIT_SCHEMA = {
    'habit_id': str,  # UUID string
    'user_id': str,  # Reference to user
    'name': str,
    'description': str,
    'category': str,
    'created_at': datetime
}

HABIT_TRACKING_SCHEMA = {
    'habit_id': str,  # Reference to habit
    'user_id': str,  # Reference to user
    'date': datetime,
    'completed': bool
}

STUDY_LOG_SCHEMA = {
    'log_id': str,  # UUID string
    'user_id': str,  # Reference to user
    'subject': str,
    'topic': str,
    'duration': int,  # in minutes
    'confidence_level': int,  # 1-5
    'notes': str,
    'created_at': datetime
}

PERSONAL_GOAL_SCHEMA = {
    'goal_id': str,  # UUID string
    'user_id': str,  # Reference to user
    'title': str,
    'description': str,
    'category': str,
    'target_date': datetime,
    'completed': bool,
    'created_at': datetime
}

PROGRESS_SCHEMA = {
    'tracking_id': str,  # UUID string
    'user_id': str,  # Reference to user
    'category': str,
    'metric': str,
    'value': float,
    'recorded_at': datetime
}