"""
Pydantic models and schemas for the appointment scheduling system.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class PatientInfo(BaseModel):
    """Patient information model."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., description="Patient email address")
    phone: str = Field(..., min_length=10, max_length=20)


class TimeSlot(BaseModel):
    """Available time slot model."""
    start_time: str
    end_time: str
    available: bool


class AvailabilityRequest(BaseModel):
    """Request model for checking availability."""
    date: str
    appointment_type: str


class AvailabilityResponse(BaseModel):
    """Response model for availability check."""
    date: str
    available_slots: List[TimeSlot]


class BookingRequest(BaseModel):
    """Request model for booking an appointment."""
    appointment_type: str
    date: str
    start_time: str
    patient: PatientInfo
    reason: Optional[str] = None


class BookingDetails(BaseModel):
    """Details of a booked appointment."""
    patient: PatientInfo
    appointment_type: str
    date: str
    start_time: str
    end_time: str
    duration_minutes: int
    reason: Optional[str] = None


class BookingResponse(BaseModel):
    """Response model for booking confirmation."""
    booking_id: str
    status: str
    confirmation_code: str
    details: BookingDetails
