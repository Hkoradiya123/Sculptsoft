from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
import json
import logging
from pathlib import Path
from core.config import SECRET_KEY, ALGORITHM


logger = logging.getLogger(__name__)


SECRET_KEY = SECRET_KEY
ALGORITHM = ALGORITHM

_here = Path(__file__).parent
EXCLUDED_PATHS = json.load(open(_here / "EXCLUDED_PATHS.json"))["EXCLUDED_PATHS"]

# Always exclude auth routes regardless of JSON content
_AUTH_ROUTES = {"/auth/login", "/auth/register"}
EXCLUDED_PATHS = list(set(EXCLUDED_PATHS) | _AUTH_ROUTES)
print(f"Excluded paths: {EXCLUDED_PATHS}")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"[AUTH] {request.method} {request.url.path}", flush=True)

        if request.url.path in EXCLUDED_PATHS or request.url.path.startswith("/auth/"):
            print(f"Skipping auth for path: {request.url.path}")
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"},
            )

        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authorization header"},
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
            )

            request.state.user_id = payload["sub"]

        except JWTError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"},
            )

        return await call_next(request)


