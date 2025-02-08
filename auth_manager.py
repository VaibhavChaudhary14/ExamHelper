import bcrypt
import uuid
from datetime import datetime
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.study_assistant_db
users = db.users

def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register_user(username: str, email: str, password: str) -> dict:
    """Register a new user"""
    # Check if username or email already exists
    if users.find_one({'$or': [{'username': username}, {'email': email}]}):
        raise ValueError("Username or email already exists")

    user_data = {
        'user_id': str(uuid.uuid4()),
        'username': username,
        'email': email,
        'password_hash': hash_password(password),
        'created_at': datetime.now(),
        'last_login': datetime.now()
    }

    users.insert_one(user_data)
    user_data.pop('password_hash')  # Remove password hash before returning
    return user_data

def authenticate_user(email: str, password: str) -> dict:
    """Authenticate a user"""
    user = users.find_one({'email': email})
    if not user:
        raise ValueError("Invalid email or password")

    if not verify_password(password, user['password_hash']):
        raise ValueError("Invalid email or password")

    # Update last login
    users.update_one(
        {'email': email},
        {'$set': {'last_login': datetime.now()}}
    )

    user.pop('password_hash')  # Remove password hash before returning
    return user

def get_user_by_id(user_id: str) -> dict:
    """Get user by ID"""
    user = users.find_one({'user_id': user_id})
    if user:
        user.pop('password_hash')  # Remove password hash before returning
    return user

def update_user_password(user_id: str, current_password: str, new_password: str) -> bool:
    """Update user password"""
    user = users.find_one({'user_id': user_id})
    if not user or not verify_password(current_password, user['password_hash']):
        raise ValueError("Invalid current password")

    users.update_one(
        {'user_id': user_id},
        {'$set': {'password_hash': hash_password(new_password)}}
    )
    return True

def update_user_profile(user_id: str, updates: dict) -> dict:
    """Update user profile information"""
    allowed_fields = {'username', 'email'}
    update_data = {k: v for k, v in updates.items() if k in allowed_fields}

    if not update_data:
        return get_user_by_id(user_id)

    users.update_one(
        {'user_id': user_id},
        {'$set': update_data}
    )

    return get_user_by_id(user_id)