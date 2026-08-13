from fastapi import FastAPI

from router.auth_router import router as auth_router
from router.complaint_router import router as complaint_router
from router.admin_router import router as admin_router
from router.agent_router import router as agent_router


app = FastAPI(
    title="Service Management and Complaint System",
    description="Complaint management API with User, Admin and Agent roles",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Service Management and Complaint System API is running"
    }


app.include_router(auth_router)
app.include_router(complaint_router)
app.include_router(admin_router)
app.include_router(agent_router)