from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from database import complaints_collection
from schemas import ComplaintCreate, ComplaintUpdate
from dependencies import get_current_user


router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)


@router.post("/")
def create_complaint(
    complaint: ComplaintCreate,
    current_user: dict = Depends(get_current_user)
):
    complaint_data = {
        "title": complaint.title,
        "description": complaint.description,
        "priority": complaint.priority,
        "status": "Pending",
        "assigned_to": None,
        "created_by": current_user["user_id"]
    }

    result = complaints_collection.insert_one(complaint_data)

    return {
        "message": "Complaint created successfully",
        "complaint_id": str(result.inserted_id)
    }


@router.get("/")
def get_complaints(
    current_user: dict = Depends(get_current_user)
):
    complaints = complaints_collection.find(
        {"created_by": current_user["user_id"]}
    )

    complaint_list = []

    for complaint in complaints:
        complaint["_id"] = str(complaint["_id"])
        complaint_list.append(complaint)

    return complaint_list


@router.get("/{complaint_id}")
def get_complaint(
    complaint_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(complaint_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid complaint ID"
        )

    complaint = complaints_collection.find_one({
        "_id": ObjectId(complaint_id),
        "created_by": current_user["user_id"]
    })

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    complaint["_id"] = str(complaint["_id"])

    return complaint


@router.put("/{complaint_id}")
def update_complaint(
    complaint_id: str,
    complaint: ComplaintUpdate,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(complaint_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid complaint ID"
        )

    existing_complaint = complaints_collection.find_one({
        "_id": ObjectId(complaint_id),
        "created_by": current_user["user_id"]
    })

    if not existing_complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    update_data = {
        key: value
        for key, value in complaint.model_dump().items()
        if value is not None
    }

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update"
        )

    complaints_collection.update_one(
        {"_id": ObjectId(complaint_id)},
        {"$set": update_data}
    )

    return {
        "message": "Complaint updated successfully"
    }