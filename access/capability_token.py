import uuid
from datetime import datetime, timedelta

# Simple in-memory token store (use DB for production)
capability_store = {}

def generate_token(user_id):
    token = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(minutes=10)
    capability_store[token] = {"user": user_id, "expires": expiry}
    return token

def validate_token(token):
    entry = capability_store.get(token)
    if entry and entry["expires"] > datetime.utcnow():
        return True
    return False