"""
Tenant context middleware for request isolation
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from app.core.auth import SECRET_KEY, ALGORITHM


class TenantContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract and set tenant context from JWT token
    """
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public endpoints
        public_paths = [
            "/api/auth/login",
            "/api/auth/signup",
            "/health",
            "/debug",
            "/docs",
            "/redoc",
            "/openapi.json"
        ]
        
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # Allow request to proceed - auth will be handled by dependencies
            return await call_next(request)
        
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # Set tenant context in request state
            request.state.tenant_id = payload.get("tenant_id")
            request.state.user_id = payload.get("sub")
            request.state.user_role = payload.get("role")
            
        except jwt.InvalidTokenError:
            # Invalid token - let auth dependencies handle it
            pass
        
        response = await call_next(request)
        return response
