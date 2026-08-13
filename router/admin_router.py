from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from database import complaints_collection, users_collection
from dependencies import admin_required


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/complaints")
def get_all_complaints(
    current_user: dict = Depends(admin_required)
):
    complaints = complaints_collection.find()

    complaint_list = []

    for complaint in complaints:
        complaint["_id"] = str(complaint["_id"])
        complaint_list.append(complaint)

    return complaint_list


@router.put("/complaints/{complaint_id}/assign/{agent_id}")
def assign_complaint(
    complaint_id: str,
    agent_id: str,
    current_user: dict = Depends(admin_required)
):
    if not ObjectId.is_valid(complaint_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid complaint ID"
        )

    if not ObjectId.is_valid(agent_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid agent ID"
        )

    agent = users_collection.find_one({
        "_id": ObjectId(agent_id),
        "role": "agent"
    })

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    complaint = complaints_collection.find_one({
        "_id": ObjectId(complaint_id)
    })

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    complaints_collection.update_one(
        {"_id": ObjectId(complaint_id)},
        {
            "$set": {
                "assigned_to": agent_id,
                "status": "Assigned"
            }
        }
    )

    return {
        "message": "Complaint assigned successfully",
        "agent_id": agent_id
    }


@router.put("/complaints/{complaint_id}/status")
def update_complaint_status(
    complaint_id: str,
    status: str,
    current_user: dict = Depends(admin_required)
):
    if not ObjectId.is_valid(complaint_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid complaint ID"
        )

    complaint = complaints_collection.find_one({
        "_id": ObjectId(complaint_id)
    })

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    complaints_collection.update_one(
        {"_id": ObjectId(complaint_id)},
        {
            "$set": {
                "status": status
            }
        }
    )

    return {
        "message": "Complaint status updated successfully",
        "status": status
    }