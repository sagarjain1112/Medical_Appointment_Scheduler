"""
Tool for checking appointment availability.
"""
from typing import List, Dict
from datetime import datetime, timedelta, time
from backend.api.calendly_integration import (
    APPOINTMENT_TYPES,
    BUSINESS_HOURS,
    generate_time_slots,
    is_slot_available
)


def check_availability(date: str, appointment_type: str) -> Dict:
    """
    Check available time slots for a given date and appointment type.
    
    Args:
        date: Date in YYYY-MM-DD format
        appointment_type: Type of appointment
        
    Returns:
        Dictionary with available slots
    """
    if appointment_type not in APPOINTMENT_TYPES:
        return {
            "success": False,
            "error": f"Invalid appointment type. Must be one of: {', '.join(APPOINTMENT_TYPES.keys())}"
        }
    
    try:
        duration = APPOINTMENT_TYPES[appointment_type]
        slots = generate_time_slots(date, duration)
        
        return {
            "success": True,
            "date": date,
            "appointment_type": appointment_type,
            "duration_minutes": duration,
            "available_slots": [
                {
                    "start_time": slot.start_time,
                    "end_time": slot.end_time,
                    "available": slot.available
                }
                for slot in slots
            ],
            "total_slots": len(slots),
            "available_count": sum(1 for slot in slots if slot.available)
        }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_business_hours() -> Dict:
    """Get clinic business hours."""
    return {
        "start": BUSINESS_HOURS["start"].strftime("%H:%M"),
        "end": BUSINESS_HOURS["end"].strftime("%H:%M")
    }


def get_appointment_types() -> Dict:
    """Get available appointment types and their durations."""
    return {
        "types": {
            name: f"{duration} minutes"
            for name, duration in APPOINTMENT_TYPES.items()
        }
    }
