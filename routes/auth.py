from flask import Blueprint, request, jsonify
from core.database import supabase
from core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from functools import wraps

auth_bp = Blueprint('auth', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = decode_token(token)
        if payload is None:
            return jsonify({'error': 'Token is invalid'}), 401
        
        request.user_id = payload.get('user_id')
        request.username = payload.get('sub')
        return f(*args, **kwargs)
    return decorated


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    response = supabase.table("users").select("*").eq("username", username).execute()
    if response.data:
        return jsonify({'error': 'Username already registered'}), 400
    
    hashed_password = get_password_hash(password)
    user_data = {
        "username": username,
        "hashed_password": hashed_password
    }
    response = supabase.table("users").insert(user_data).execute()
    return jsonify(response.data[0])


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    response = supabase.table("users").select("*").eq("username", username).execute()
    if not response.data:
        return jsonify({'error': 'Incorrect username or password'}), 401
    
    user = response.data[0]
    if not verify_password(password, user["hashed_password"]):
        return jsonify({'error': 'Incorrect username or password'}), 401
    
    access_token = create_access_token(data={"sub": user["username"], "user_id": str(user["id"])})
    refresh_token = create_refresh_token(data={"sub": user["username"], "user_id": str(user["id"])})
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    })


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        return jsonify({'error': 'Refresh token required'}), 400
    
    payload = decode_token(refresh_token)
    if payload is None:
        return jsonify({'error': 'Invalid refresh token'}), 401
    
    username = payload.get("sub")
    if not username:
        return jsonify({'error': 'Invalid refresh token'}), 401
    
    response = supabase.table("users").select("*").eq("username", username).execute()
    if not response.data:
        return jsonify({'error': 'User not found'}), 401
    
    user = response.data[0]
    access_token = create_access_token(data={"sub": username, "user_id": str(user["id"])})
    new_refresh_token = create_refresh_token(data={"sub": username, "user_id": str(user["id"])})
    return jsonify({
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    })
