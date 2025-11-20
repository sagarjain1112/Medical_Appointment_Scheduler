"""
Integration tests for the appointment scheduling agent.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from backend.main import app
from backend.api.calendly_integration import booked_appointments

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_bookings():
    """Clear bookings before each test."""
    booked_appointments.clear()
    yield
    booked_appointments.clear()


class TestAvailabilityEndpoint:
    """Tests for the availability checking endpoint."""

    def test_get_availability_valid_date(self):
        """Test getting availability for a valid future date."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        response = client.get(
            f"/api/calendly/availability?date={tomorrow}&appointment_type=consultation"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["date"] == tomorrow
        assert isinstance(data["available_slots"], list)
        assert len(data["available_slots"]) > 0

    def test_get_availability_past_date(self):
        """Test getting availability for a past date returns empty slots."""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        response = client.get(
            f"/api/calendly/availability?date={yesterday}&appointment_type=consultation"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["available_slots"]) == 0

    def test_get_availability_invalid_appointment_type(self):
        """Test getting availability with invalid appointment type."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        response = client.get(
            f"/api/calendly/availability?date={tomorrow}&appointment_type=invalid"
        )
        assert response.status_code == 400

    def test_get_availability_invalid_date_format(self):
        """Test getting availability with invalid date format."""
        response = client.get(
            "/api/calendly/availability?date=2025/11/21&appointment_type=consultation"
        )
        assert response.status_code == 400

    def test_get_availability_all_appointment_types(self):
        """Test getting availability for all appointment types."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        appointment_types = ["consultation", "followup", "physical", "specialist"]

        for appt_type in appointment_types:
            response = client.get(
                f"/api/calendly/availability?date={tomorrow}&appointment_type={appt_type}"
            )
            assert response.status_code == 200
            data = response.json()
            assert data["date"] == tomorrow
            assert len(data["available_slots"]) > 0


class TestBookingEndpoint:
    """Tests for the booking endpoint."""

    def test_book_appointment_success(self):
        """Test successful appointment booking."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        # First, get available slots
        response = client.get(
            f"/api/calendly/availability?date={tomorrow}&appointment_type=consultation"
        )
        assert response.status_code == 200
        available_slots = response.json()["available_slots"]
        assert len(available_slots) > 0

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

        response = client.post("/api/calendly/book", json=booking_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "confirmed"
        assert "booking_id" in data
        assert "confirmation_code" in data
        assert data["details"]["appointment_type"] == "consultation"
        assert data["details"]["date"] == tomorrow
        assert data["details"]["start_time"] == slot["start_time"]

    def test_book_appointment_double_booking(self):
        """Test that double-booking is prevented."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        # Get available slots
        response = client.get(
            f"/api/calendly/availability?date={tomorrow}&appointment_type=consultation"
        )
        available_slots = response.json()["available_slots"]
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

        # First booking should succeed
        response = client.post("/api/calendly/book", json=booking_data)
        assert response.status_code == 200

        # Second booking at same time should fail
        booking_data["patient"]["name"] = "Jane Doe"
        booking_data["patient"]["email"] = "jane@example.com"
        response = client.post("/api/calendly/book", json=booking_data)
        assert response.status_code == 409

    def test_book_appointment_invalid_type(self):
        """Test booking with invalid appointment type."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        booking_data = {
            "appointment_type": "invalid",
            "date": tomorrow,
            "start_time": "10:00",
            "patient": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1-555-1234"
            }
        }

        response = client.post("/api/calendly/book", json=booking_data)
        assert response.status_code == 400

    def test_book_appointment_past_date(self):
        """Test booking with past date."""
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

    def test_book_appointment_missing_fields(self):
        """Test booking with missing required fields."""
        response = client.post("/api/calendly/book", json={"appointment_type": "consultation"})
        assert response.status_code == 422  # Validation error

    def test_book_appointment_all_types(self):
        """Test booking for all appointment types."""
        appointment_types = ["consultation", "followup", "physical", "specialist"]

        for idx, appt_type in enumerate(appointment_types):
            # Use different dates to avoid conflicts
            date = (datetime.now() + timedelta(days=idx+1)).strftime("%Y-%m-%d")
            
            # Get available slots
            response = client.get(
                f"/api/calendly/availability?date={date}&appointment_type={appt_type}"
            )
            available_slots = response.json()["available_slots"]

            if available_slots:
                slot = available_slots[0]
                booking_data = {
                    "appointment_type": appt_type,
                    "date": date,
                    "start_time": slot["start_time"],
                    "patient": {
                        "name": f"Patient {appt_type}",
                        "email": f"{appt_type}@example.com",
                        "phone": "+1-555-1234"
                    }
                }

                response = client.post("/api/calendly/book", json=booking_data)
                assert response.status_code == 200


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestSlotGeneration:
    """Tests for time slot generation logic."""

    def test_slot_duration_consultation(self):
        """Test that consultation slots are 30 minutes."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        response = client.get(
            f"/api/calendly/availability?date={tomorrow}&appointment_type=consultation"
        )
        slots = response.json()["available_slots"]

        for slot in slots:
            start = datetime.strptime(slot["start_time"], "%H:%M")
            end = datetime.strptime(slot["end_time"], "%H:%M")
            duration = (end - start).total_seconds() / 60
            assert duration == 30

    def test_slot_duration_followup(self):
        """Test that follow-up slots are 15 minutes."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        response = client.get(
            f"/api/calendly/availability?date={tomorrow}&appointment_type=followup"
        )
        slots = response.json()["available_slots"]

        for slot in slots:
            start = datetime.strptime(slot["start_time"], "%H:%M")
            end = datetime.strptime(slot["end_time"], "%H:%M")
            duration = (end - start).total_seconds() / 60
            assert duration == 15

    def test_slot_within_business_hours(self):
        """Test that all slots are within business hours."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        response = client.get(
            f"/api/calendly/availability?date={tomorrow}&appointment_type=consultation"
        )
        slots = response.json()["available_slots"]

        for slot in slots:
            start_time = datetime.strptime(slot["start_time"], "%H:%M").time()
            assert start_time >= datetime.strptime("09:00", "%H:%M").time()
            assert start_time < datetime.strptime("17:00", "%H:%M").time()

    def test_today_slots_only_show_remaining_time(self):
        """Test that today's date only shows remaining time slots."""
        today = datetime.now().strftime("%Y-%m-%d")
        response = client.get(
            f"/api/calendly/availability?date={today}&appointment_type=consultation"
        )
        assert response.status_code == 200
        slots = response.json()["available_slots"]
        
        # Get current time rounded up to next 15-minute interval
        now = datetime.now()
        minutes = now.minute
        if minutes % 15 != 0:
            minutes = ((minutes // 15) + 1) * 15
        if minutes == 60:
            earliest_slot_time = (now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)).time()
        else:
            earliest_slot_time = now.replace(minute=minutes, second=0, microsecond=0).time()
        
        # Ensure earliest slot is not before current time
        if slots:
            first_slot_time = datetime.strptime(slots[0]["start_time"], "%H:%M").time()
            assert first_slot_time >= earliest_slot_time


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
