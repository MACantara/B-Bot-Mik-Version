from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.database import supabase
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.schemas.user import UserCreate, UserLogin, Token, User as UserSchema

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    response = supabase.table("users").select("*").eq("username", username).execute()
    if not response.data:
        raise credentials_exception
    return response.data[0]


@router.post("/register", response_model=UserSchema)
def register(user: UserCreate):
    response = supabase.table("users").select("*").eq("username", user.username).execute()
    if response.data:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    user_data = {
        "username": user.username,
        "hashed_password": hashed_password
    }
    response = supabase.table("users").insert(user_data).execute()
    return response.data[0]


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin):
    response = supabase.table("users").select("*").eq("username", user_credentials.username).execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = response.data[0]
    if not verify_password(user_credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"], "user_id": str(user["id"])})
    refresh_token = create_refresh_token(data={"sub": user["username"], "user_id": str(user["id"])})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str):
    payload = decode_token(refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    response = supabase.table("users").select("*").eq("username", username).execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    user = response.data[0]
    access_token = create_access_token(data={"sub": username, "user_id": str(user["id"])})
    new_refresh_token = create_refresh_token(data={"sub": username, "user_id": str(user["id"])})
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
