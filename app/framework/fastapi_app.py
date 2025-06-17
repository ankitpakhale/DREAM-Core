from fastapi import FastAPI, Request, Response  # used in some other files
import uvicorn  # used in some other files
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI(
    title="DREAM",
    description="Dynamic Realization Engine for Achieving Milestones",
    version="1.0.0",
    openapi_version="1.0.0",
)

# Expose FastAPI framework components
App = app

# Configure CORS
App.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # specify origin for frontend like ["https://finddreamlife.com"]
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


@App.get("/openapi.json")
def get_openapi():
    return JSONResponse(content=app.openapi())
