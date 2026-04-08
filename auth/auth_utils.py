import bcrypt
from database.db_utils import get_user_by_username, create_user, get_user_by_email

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a password against a hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(username, password):
    """Checks if username and password match."""
    user = get_user_by_username(username)
    if user and verify_password(password, user['password_hash']):
        return user
    return None

def register_user(username, email, password):
    """Registers a new user."""
    hashed_password = hash_password(password)
    return create_user(username, email, hashed_password)

def get_or_create_google_user(email: str, name: str):
    """Logs in via email. If user doesn't exist, safely autoregisters them."""
    user = get_user_by_email(email)
    if user:
        return user
        
    import secrets
    # Generate random username if needed, or fallback to name
    base_username = name.replace(" ", "").lower()
    if not base_username: 
        base_username = "google_user"
    username = f"{base_username}_{secrets.token_hex(4)}"
    
    # Generate unguessable password
    dummy_password = secrets.token_urlsafe(32)
    success, identifier = register_user(username, email, dummy_password)
    
    if success:
        from database.db_utils import update_user_profile
        update_user_profile(identifier, display_name=name)
        return get_user_by_email(email)
    return None
