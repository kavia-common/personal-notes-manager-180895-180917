from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.notes import router as notes_router

openapi_tags = [
    {
        "name": "Health",
        "description": "Service health and operational endpoints",
    },
    {
        "name": "Notes",
        "description": "Create, read, update and delete notes",
    },
]

app = FastAPI(
    title="Personal Notes API",
    description="A simple notes service with CRUD operations and basic auth scaffolding.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict origins in production using env config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Returns service health information.",
)
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}


# Register routers
app.include_router(notes_router)
