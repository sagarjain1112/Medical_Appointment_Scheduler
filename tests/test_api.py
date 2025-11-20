import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from backend.main import app

client = TestClient(app)

def test_get_availability():
    # Test with valid date and appointment type
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = client.get(f"/api/calendly/availability?date={tomorrow}&appointment_type=consultation")
    assert response.status_code == 200
    data = response.json()
    assert data["date"] == tomorrow
    assert isinstance(data["available_slots"], list)
    
    # Test with invalid appointment type
    response = client.get(f"/api/calendly/availability?date={tomorrow}&appointment_type=invalid")
    assert response.status_code == 400
    
    # Test with past date
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    response = client.get(f"/api/calendly/availability?date={yesterday}&appointment_type=consultation")
    assert response.status_code == 200
    assert len(response.json()["available_slots"]) == 0

def test_book_appointment():
    # First, get available slots
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = client.get(f"/api/calendly/availability?date={tomorrow}&appointment_type=consultation")
    assert response.status_code == 200
    available_slots = response.json()["available_slots"]
    
    if available_slots:
        # Book the first available slot
        slot = available_slots[0]
        booking_data = {
            "appointment_type": "consultation",
            "date": tomorrow,
            "start_time": slot["start_time"],
            "patient": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1-555-1234"
            },
            "reason": "Routine checkup"
        }
        
        # Test successful booking
        response = client.post("/api/calendly/book", json=booking_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "confirmed"
        assert "booking_id" in data
        assert "confirmation_code" in data
        
        # Try to book the same slot again (should fail)
        response = client.post("/api/calendly/book", json=booking_data)
        assert response.status_code == 409
        
        # Test with invalid appointment type
        invalid_booking = booking_data.copy()
        invalid_booking["appointment_type"] = "invalid"
        response = client.post("/api/calendly/book", json=invalid_booking)
        assert response.status_code == 400
    else:
        pytest.skip("No available slots to test booking")

def test_booking_validation():
    # Test with missing required fields
    response = client.post("/api/calendly/book", json={"appointment_type": "consultation"})
    assert response.status_code == 422  # Validation error
    
    # Test with past date
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    booking_data = {
        "appointment_type": "consultation",
        "date": yesterday,
        "start_time": "10:00",
        "patient": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1-555-1234"
        }
    }
    response = client.post("/api/calendly/book", json=booking_data)
    assert response.status_code == 400
