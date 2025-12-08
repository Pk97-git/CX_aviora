"""
Admin API routes for user and tenant management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

from app.core.database import get_db
from app.core.auth import (
    get_current_user,
    get_current_tenant,
    require_role,
    get_password_hash
)
from app.models.tenant import User, Tenant, Integration, APIKey

router = APIRouter()


# Request/Response Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str  # 'admin', 'manager', 'agent'


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    settings: Optional[dict] = None


class IntegrationCreate(BaseModel):
    type: str  # 'freshdesk', 'jira', 'slack'
    name: str
    config: dict


class IntegrationResponse(BaseModel):
    id: str
    type: str
    name: str
    status: str
    last_sync_at: Optional[datetime]
    created_at: datetime


# User Management
@router.get("/users", response_model=List[UserResponse])
async def list_users(
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(require_role('manager')),
    db: AsyncSession = Depends(get_db)
):
    """List all users in the tenant"""
    result = await db.execute(
        select(User).where(User.tenant_id == tenant.id).order_by(User.created_at.desc())
    )
    users = result.scalars().all()
    
    return [
        UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at
        )
        for user in users
    ]


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserCreate,
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(require_role('admin')),
    db: AsyncSession = Depends(get_db)
):
    """Create a new user in the tenant"""
    # Check if email already exists
    result = await db.execute(
        select(User).where(
            User.tenant_id == tenant.id,
            User.email == request.email
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Create user
    user = User(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        email=request.email,
        password_hash=get_password_hash(request.password),
        full_name=request.full_name,
        role=request.role,
        is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at
    )


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    request: UserUpdate,
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(require_role('admin')),
    db: AsyncSession = Depends(get_db)
):
    """Update a user"""
    result = await db.execute(
        select(User).where(
            User.id == user_id,
            User.tenant_id == tenant.id
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    if request.full_name is not None:
        user.full_name = request.full_name
    if request.role is not None:
        user.role = request.role
    if request.is_active is not None:
        user.is_active = request.is_active
    
    user.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(require_role('admin')),
    db: AsyncSession = Depends(get_db)
):
    """Delete a user"""
    # Prevent deleting yourself
    if str(current_user.id) == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    result = await db.execute(
        delete(User).where(
            User.id == user_id,
            User.tenant_id == tenant.id
        )
    )
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await db.commit()


# Tenant Management
@router.get("/tenant")
async def get_tenant(
    tenant: Tenant = Depends(get_current_tenant)
):
    """Get current tenant information"""
    return {
        "id": str(tenant.id),
        "name": tenant.name,
        "slug": tenant.slug,
        "plan": tenant.plan,
        "status": tenant.status,
        "settings": tenant.settings,
        "created_at": tenant.created_at
    }


@router.put("/tenant")
async def update_tenant(
    request: TenantUpdate,
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(require_role('admin')),
    db: AsyncSession = Depends(get_db)
):
    """Update tenant settings"""
    if request.name is not None:
        tenant.name = request.name
    if request.settings is not None:
        tenant.settings = request.settings
    
    tenant.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(tenant)
    
    return {
        "id": str(tenant.id),
        "name": tenant.name,
        "slug": tenant.slug,
        "plan": tenant.plan,
        "settings": tenant.settings
    }


# Integration Management
@router.get("/integrations", response_model=List[IntegrationResponse])
async def list_integrations(
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all integrations"""
    result = await db.execute(
        select(Integration).where(Integration.tenant_id == tenant.id)
    )
    integrations = result.scalars().all()
    
    return [
        IntegrationResponse(
            id=str(integration.id),
            type=integration.type,
            name=integration.name,
            status=integration.status,
            last_sync_at=integration.last_sync_at,
            created_at=integration.created_at
        )
        for integration in integrations
    ]


@router.post("/integrations", response_model=IntegrationResponse, status_code=status.HTTP_201_CREATED)
async def create_integration(
    request: IntegrationCreate,
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(require_role('admin')),
    db: AsyncSession = Depends(get_db)
):
    """Create a new integration"""
    integration = Integration(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        type=request.type,
        name=request.name,
        config=request.config,
        status='active'
    )
    db.add(integration)
    await db.commit()
    await db.refresh(integration)
    
    return IntegrationResponse(
        id=str(integration.id),
        type=integration.type,
        name=integration.name,
        status=integration.status,
        last_sync_at=integration.last_sync_at,
        created_at=integration.created_at
    )


@router.delete("/integrations/{integration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_integration(
    integration_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    current_user: User = Depends(require_role('admin')),
    db: AsyncSession = Depends(get_db)
):
    """Delete an integration"""
    result = await db.execute(
        delete(Integration).where(
            Integration.id == integration_id,
            Integration.tenant_id == tenant.id
        )
    )
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    await db.commit()
