from fastapi import HTTPException

def verify_token(token: str):
    if token != "expected_token":
        raise HTTPException(status_code=400, detail="Invalid Token")