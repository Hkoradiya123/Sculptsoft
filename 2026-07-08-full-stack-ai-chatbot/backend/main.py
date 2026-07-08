from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from core.exceptions import AppException, app_exception_handler
from middleware.auth import AuthMiddleware
from api import auth, users, conversations, messages, chat

app = FastAPI(
    title="ai-chatbot-backend",
    description="AI Chatbot backend API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT auth guard
app.add_middleware(AuthMiddleware)

# Exception handler
app.add_exception_handler(AppException, app_exception_handler)

# Routers
app.include_router(auth.router,          prefix="/auth",          tags=["auth"])
app.include_router(users.router,         prefix="/users",         tags=["users"])
app.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
app.include_router(messages.router,      prefix="/messages",      tags=["messages"])
app.include_router(chat.router,          prefix="/chat",          tags=["chat"])


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
