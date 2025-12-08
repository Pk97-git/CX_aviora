"""
Authentication and user management API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

from app.core.database import get_db
from app.core.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_current_tenant
)
from app.models.tenant import User, Tenant

router = APIRouter()


# Request/Response Models
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    tenant_name: str
    tenant_slug: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    """
    Create a new tenant and admin user
    """
    # Check if tenant slug already exists
    result = await db.execute(
        select(Tenant).where(Tenant.slug == request.tenant_slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant slug already exists"
        )
    
    # Create tenant
    tenant = Tenant(
        id=uuid.uuid4(),
        name=request.tenant_name,
        slug=request.tenant_slug,
        plan='free',
        status='active'
    )
    db.add(tenant)
    await db.flush()  # Get the tenant ID
    
    # Check if user email already exists for this tenant
    result = await db.execute(
        select(User).where(
            User.tenant_id == tenant.id,
            User.email == request.email
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create admin user
    user = User(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        email=request.email,
        password_hash=get_password_hash(request.password),
        full_name=request.full_name,
        role='admin',
        is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Create tokens
    token_data = {
        "sub": str(user.id),
        "tenant_id": str(tenant.id),
        "email": user.email,
        "role": user.role
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "tenant_id": str(tenant.id),
            "tenant_name": tenant.name
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and return tokens
    """
    # Find user by email (across all tenants)
    result = await db.execute(
        select(User).where(User.email == request.email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Get tenant
    result = await db.execute(
        select(Tenant).where(Tenant.id == user.tenant_id)
    )
    tenant = result.scalar_one_or_none()
    
    if not tenant or tenant.status != 'active':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant account is not active"
        )
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    await db.commit()
    
    # Create tokens
    token_data = {
        "sub": str(user.id),
        "tenant_id": str(tenant.id),
        "email": user.email,
        "role": user.role
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "tenant_id": str(tenant.id),
            "tenant_name": tenant.name
        }
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    """
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """
    Refresh access token using refresh token
    """
    from jose import jwt, JWTError
    from app.core.auth import SECRET_KEY, ALGORITHM
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")
        
        # Fetch user
        result = await db.execute(
            select(User).where(User.id == user_id, User.tenant_id == tenant_id)
        )
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Get tenant
        result = await db.execute(
            select(Tenant).where(Tenant.id == tenant_id)
        )
        tenant = result.scalar_one_or_none()
        
        # Create new tokens
        token_data = {
            "sub": str(user.id),
            "tenant_id": str(tenant.id),
            "email": user.email,
            "role": user.role
        }
        new_access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            user={
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "tenant_id": str(tenant.id),
                "tenant_name": tenant.name
            }
        )
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
