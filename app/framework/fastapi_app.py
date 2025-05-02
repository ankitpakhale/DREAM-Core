from fastapi import FastAPI, Request, Response
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI()

# Expose FastAPI framework components
App = app

# Configure CORS
App.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify origins like ["https://example.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Origin",
        "Content-Type",
        "Accept",
        "Authorization",
        "X-Is-Feedback-Loop",
        "X-Active-Client",
        "X-Is-Compare-Mode",
    ],
)


# Sample route to test server
@App.get("/")
def read_root():
    return {"message": "FastAPI CORS-configured app"}
