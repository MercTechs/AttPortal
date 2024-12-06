from fastapi import HTTPException, Request
from src.app.core.config import settings

def get_access_code():
    """Retrieve access code from settings"""
    # In a real application, this should be properly hashed and stored securely
    return settings.ACCESS_CODE

async def verify_access_code(request: Request):
    """Dependency function to verify access code"""
    access_code = request.headers.get('X-Access-Code')
    
    if not access_code:
        raise HTTPException(
            status_code=401,
            detail="Access code is required"
        )
    
    if access_code != get_access_code():
        raise HTTPException(
            status_code=403,
            detail="Invalid access code"
        )
    
    return True