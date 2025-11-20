"""
Chat API endpoints for the scheduling agent.
"""
from fastapi import APIRouter, HTTPException
from .calendly_integration import (
    APPOINTMENT_TYPES,
    generate_time_slots,
    book_appointment,
    BookingRequest,
    BookingResponse,
    TimeSlot
)
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/calendly", tags=["calendly"])


class AvailabilityRequest(BaseModel):
    date: str
    appointment_type: str


class AvailabilityResponse(BaseModel):
    date: str
    available_slots: List[TimeSlot]


@router.get("/availability", response_model=AvailabilityResponse)
async def get_availability(date: str, appointment_type: str):
    """
    Get available time slots for a specific date and appointment type.
    
    - **date**: Date in YYYY-MM-DD format
    - **appointment_type**: Type of appointment (consultation, followup, physical, specialist)
    """
    if appointment_type not in APPOINTMENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid appointment type. Must be one of: {', '.join(APPOINTMENT_TYPES.keys())}"
        )
    
    try:
        duration = APPOINTMENT_TYPES[appointment_type]
        slots = generate_time_slots(date, duration)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "date": date,
        "available_slots": slots
    }


@router.post("/book", response_model=BookingResponse)
async def book_appointment_endpoint(booking: BookingRequest):
    """
    Book an appointment.
    
    - **appointment_type**: Type of appointment
    - **date**: Appointment date in YYYY-MM-DD format
    - **start_time**: Start time in HH:MM format (24-hour)
    - **patient**: Patient information
    - **reason**: Optional reason for the visit
    """
    if booking.appointment_type not in APPOINTMENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid appointment type. Must be one of: {', '.join(APPOINTMENT_TYPES.keys())}"
        )
    
    try:
        response = book_appointment(booking)
        return response
    except ValueError as e:
        if "no longer available" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
