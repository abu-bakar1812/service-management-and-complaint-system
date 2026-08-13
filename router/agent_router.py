from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from database import complaints_collection
from dependencies import agent_required


router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)


@router.get("/complaints")
def get_assigned_complaints(
    current_user: dict = Depends(agent_required)
):
    agent_id = current_user["user_id"]

    complaints = complaints_collection.find({
        "assigned_to": agent_id
    })

    complaint_list = []

    for complaint in complaints:
        complaint["_id"] = str(complaint["_id"])
        complaint_list.append(complaint)

    return complaint_list


@router.get("/complaints/{complaint_id}")
def get_assigned_complaint(
    complaint_id: str,
    current_user: dict = Depends(agent_required)
):
    if not ObjectId.is_valid(complaint_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid complaint ID"
        )

    complaint = complaints_collection.find_one({
        "_id": ObjectId(complaint_id),
        "assigned_to": current_user["user_id"]
    })

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found or not assigned to you"
        )

    complaint["_id"] = str(complaint["_id"])

    return complaint


@router.put("/complaints/{complaint_id}/status")
def update_assigned_complaint_status(
    complaint_id: str,
    status: str,
    current_user: dict = Depends(agent_required)
):
    if not ObjectId.is_valid(complaint_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid complaint ID"
        )

    complaint = complaints_collection.find_one({
        "_id": ObjectId(complaint_id),
        "assigned_to": current_user["user_id"]
    })

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found or not assigned to you"
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