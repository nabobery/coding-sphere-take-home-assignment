from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api import auth_router, project_router
from sqlmodel import Session, text
from core.db import get_session, create_db_and_tables
from contextlib import asynccontextmanager
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="FastAPI JWT RBAC API", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(project_router, prefix="/api/v1/project", tags=["Projects"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI JWT RBAC API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Add a test endpoint to check database 
@app.get("/db-test")
def test_db(session: Session = Depends(get_session)):
    try:
        # Just execute a simple query
        session.exec(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)