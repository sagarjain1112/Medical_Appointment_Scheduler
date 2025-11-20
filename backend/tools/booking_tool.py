"""
Tool for booking appointments.
"""
from typing import Dict, Optional
from backend.api.calendly_integration import (
    book_appointment,
    BookingRequest,
    PatientInfo,
    APPOINTMENT_TYPES
)


def create_booking(
    appointment_type: str,
    date: str,
    start_time: str,
    patient_name: str,
    patient_email: str,
    patient_phone: str,
    reason: Optional[str] = None
) -> Dict:
    """
    Create a new appointment booking.
    
    Args:
        appointment_type: Type of appointment
        date: Date in YYYY-MM-DD format
        start_time: Start time in HH:MM format
        patient_name: Patient's full name
        patient_email: Patient's email
        patient_phone: Patient's phone number
        reason: Optional reason for visit
        
    Returns:
        Dictionary with booking confirmation details
    """
    if appointment_type not in APPOINTMENT_TYPES:
        return {
            "success": False,
            "error": f"Invalid appointment type. Must be one of: {', '.join(APPOINTMENT_TYPES.keys())}"
        }
    
    try:
        patient = PatientInfo(
            name=patient_name,
            email=patient_email,
            phone=patient_phone
        )
        
        booking_request = BookingRequest(
            appointment_type=appointment_type,
            date=date,
            start_time=start_time,
            patient=patient,
            reason=reason
        )
        
        response = book_appointment(booking_request)
        
        return {
            "success": True,
            "booking_id": response.booking_id,
            "status": response.status,
            "confirmation_code": response.confirmation_code,
            "details": response.details
        }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Booking failed: {str(e)}"
        }


def validate_booking_request(
    appointment_type: str,
    date: str,
    start_time: str,
    patient_name: str,
    patient_email: str,
    patient_phone: str
) -> Dict:
    """
    Validate booking request parameters.
    
    Args:
        appointment_type: Type of appointment
        date: Date in YYYY-MM-DD format
        start_time: Start time in HH:MM format
        patient_name: Patient's full name
        patient_email: Patient's email
        patient_phone: Patient's phone number
        
    Returns:
        Dictionary with validation results
    """
    errors = []
    
    if not appointment_type or appointment_type not in APPOINTMENT_TYPES:
        errors.append(f"Invalid appointment type: {appointment_type}")
    
    if not date:
        errors.append("Date is required")
    
    if not start_time:
        errors.append("Start time is required")
    
    if not patient_name or len(patient_name.strip()) == 0:
        errors.append("Patient name is required")
    
    if not patient_email or "@" not in patient_email:
        errors.append("Valid email is required")
    
    if not patient_phone or len(patient_phone.strip()) < 10:
        errors.append("Valid phone number is required")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
