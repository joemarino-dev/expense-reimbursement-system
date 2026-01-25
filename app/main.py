"""
FastAPI application entry point for the Expense Reimbursement System.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import expenses

app = FastAPI(
    title="Expense Reimbursement System",
    description="API for managing expense submissions, approvals, and notifications",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.include_router(expenses.router)

@app.get("/")
async def root():
    """Root endpoint - basic health check."""
    return {
        "message": "Expense Reimbursement System API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}