"""
Calendly API integration module for handling appointment scheduling.
"""
from datetime import datetime, timedelta, time
from typing import List, Optional, Dict
from pydantic import BaseModel

# Constants
BUSINESS_HOURS = {
    "start": time(9, 0),    # 9:00 AM
    "end": time(17, 0),     # 5:00 PM
}

APPOINTMENT_TYPES = {
    "consultation": 30,     # 30 minutes
    "followup": 15,         # 15 minutes
    "physical": 45,         # 45 minutes
    "specialist": 60,       # 60 minutes
}

# In-memory storage for booked appointments
booked_appointments: Dict[str, dict] = {}


class TimeSlot(BaseModel):
    start_time: str
    end_time: str
    available: bool


class PatientInfo(BaseModel):
    name: str
    email: str
    phone: str


class BookingRequest(BaseModel):
    appointment_type: str
    date: str
    start_time: str
    patient: PatientInfo
    reason: Optional[str] = None


class BookingResponse(BaseModel):
    booking_id: str
    status: str
    confirmation_code: str
    details: dict


def generate_time_slots(date_str: str, appointment_duration: int) -> List[TimeSlot]:
    """Generate available time slots for a given date and duration."""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    if date < datetime.now().date():
        return []
    
    # Generate slots for the day
    slots = []
    current_time = datetime.combine(date, BUSINESS_HOURS["start"])
    end_time = datetime.combine(date, BUSINESS_HOURS["end"])
    
    # If the selected date is today, start from current time (rounded up to next 15-min slot)
    now = datetime.now()
    if date == now.date():
        # Round up to the next 15-minute interval
        minutes = now.minute
        if minutes % 15 != 0:
            minutes = ((minutes // 15) + 1) * 15
        if minutes == 60:
            current_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            current_time = now.replace(minute=minutes, second=0, microsecond=0)
        
        # Ensure we don't start before business hours
        if current_time.time() < BUSINESS_HOURS["start"]:
            current_time = datetime.combine(date, BUSINESS_HOURS["start"])
    
    while current_time + timedelta(minutes=appointment_duration) <= end_time:
        slot_end = current_time + timedelta(minutes=appointment_duration)
        
        # Check if slot is already booked
        slot_key = f"{current_time.strftime('%Y-%m-%d %H:%M')}"
        is_booked = slot_key in booked_appointments
        
        slots.append(TimeSlot(
            start_time=current_time.strftime("%H:%M"),
            end_time=slot_end.strftime("%H:%M"),
            available=not is_booked
        ))
        
        # Move to next slot (by appointment duration to avoid overlaps)
        current_time += timedelta(minutes=appointment_duration)
    
    return slots


def is_slot_available(date: str, start_time: str, duration: int) -> bool:
    """Check if a specific time slot is available."""
    start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + timedelta(minutes=duration)
    
    # Check against booked appointments
    check_time = start_dt
    while check_time < end_dt:
        if f"{check_time.strftime('%Y-%m-%d %H:%M')}" in booked_appointments:
            return False
        check_time += timedelta(minutes=15)
    
    return True


def generate_booking_id() -> str:
    """Generate a unique booking ID."""
    import random
    return f"APPT-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"


def generate_confirmation_code() -> str:
    """Generate a random confirmation code."""
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def book_appointment(booking: BookingRequest) -> BookingResponse:
    """Book an appointment and store it."""
    duration = APPOINTMENT_TYPES[booking.appointment_type]
    
    # Validate date and time
    try:
        start_dt = datetime.strptime(f"{booking.date} {booking.start_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Invalid date or time format")
    
    if start_dt < datetime.now():
        raise ValueError("Cannot book appointments in the past")
    
    # Check if slot is still available
    if not is_slot_available(booking.date, booking.start_time, duration):
        raise ValueError("The selected time slot is no longer available")
    
    # Generate booking details
    booking_id = generate_booking_id()
    confirmation_code = generate_confirmation_code()
    
    # Mark time slots as booked
    current_time = start_dt
    end_time = start_dt + timedelta(minutes=duration)
    while current_time < end_time:
        booked_appointments[f"{current_time.strftime('%Y-%m-%d %H:%M')}"] = {
            "booking_id": booking_id,
            "patient": booking.patient.model_dump(),
            "appointment_type": booking.appointment_type,
            "reason": booking.reason
        }
        current_time += timedelta(minutes=15)
    
    # Prepare response
    return BookingResponse(
        booking_id=booking_id,
        status="confirmed",
        confirmation_code=confirmation_code,
        details={
            "patient": booking.patient.model_dump(),
            "appointment_type": booking.appointment_type,
            "date": booking.date,
            "start_time": booking.start_time,
            "end_time": (start_dt + timedelta(minutes=duration)).strftime("%H:%M"),
            "duration_minutes": duration,
            "reason": booking.reason
        }
    )
