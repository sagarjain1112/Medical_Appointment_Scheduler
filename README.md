# Medical Appointment Scheduling Agent - Calendly Integration

This module implements the **Calendly Integration** component for a medical appointment scheduling system. It provides mock API endpoints for checking availability and booking appointments, along with a modern React frontend for a complete full-stack solution.

## Overview

This is a production-ready implementation of the Calendly Integration module from the Medical Appointment Scheduling Agent assessment. It includes:

- Mock Calendly API endpoints
- Intelligent scheduling logic
- Beautiful React UI
- Comprehensive testing
- Clean modular architecture

## Features

- **Appointment Type Support**: Consultation (30min), Follow-up (15min), Physical Exam (45min), Specialist (60min)
- **Smart Availability**: Automatic slot generation with conflict detection
- **Real-time Booking**: Instant confirmation with unique booking IDs
- **Beautiful UI**: Modern React interface with smooth animations
- **Form Validation**: Client and server-side validation
- **Error Handling**: Graceful handling of edge cases
- **RESTful API**: Clean, well-documented endpoints
- **Comprehensive Tests**: Full test coverage

## Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: React 18
- **API Communication**: Axios
- **Styling**: CSS3 with gradients
- **Testing**: Pytest

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```
   
   Backend available at: `http://127.0.0.1:8000`
   
   API docs available at: `http://127.0.0.1:8000/docs`

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```
   
   Frontend opens at: `http://localhost:3000`

## API Endpoints

### Get Available Slots

```http
GET /api/calendly/availability?date=2025-11-21&appointment_type=consultation
```

**Parameters:**
- `date` (required): Date in YYYY-MM-DD format
- `appointment_type` (required): One of `consultation`, `followup`, `physical`, `specialist`

**Response:**
```json
{
  "date": "2025-11-21",
  "available_slots": [
    {
      "start_time": "09:00",
      "end_time": "09:30",
      "available": true
    },
    {
      "start_time": "09:30",
      "end_time": "10:00",
      "available": false
    }
  ]
}
```

### Book Appointment

```http
POST /api/calendly/book
Content-Type: application/json
```

**Request Body:**
```json
{
  "appointment_type": "consultation",
  "date": "2025-11-21",
  "start_time": "10:00",
  "patient": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-1234"
  },
  "reason": "Routine checkup"
}
```

**Response (200 OK):**
```json
{
  "booking_id": "APPT-20251120-5432",
  "status": "confirmed",
  "confirmation_code": "ABC123",
  "details": {
    "patient": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-1234"
    },
    "appointment_type": "consultation",
    "date": "2025-11-21",
    "start_time": "10:00",
    "end_time": "10:30",
    "duration_minutes": 30,
    "reason": "Routine checkup"
  }
}
```

**Error Responses:**
- `400`: Invalid appointment type or date format
- `409`: Slot no longer available (double-booking prevented)
- `422`: Missing or invalid patient information

## Appointment Types

| Type | Duration | Use Case |
|------|----------|----------|
| Consultation | 30 min | General medical consultation |
| Follow-up | 15 min | Quick follow-up visits |
| Physical | 45 min | Physical examination |
| Specialist | 60 min | Specialist consultation |

## Business Hours

- **Monday - Friday**: 9:00 AM - 5:00 PM
- **Time Slot Interval**: 15 minutes
- **Future Support**: Saturday hours and timezone handling

## Testing

Run the complete test suite:

```bash
pytest tests/ -v
```

Test coverage includes:
- Availability checking
- Booking creation
- Double-booking prevention
- Input validation
- Error handling
- All appointment types
- Business hours validation

## Project Structure

```
appointment-scheduling-agent/
├── README.md                          # This file
├── ARCHITECTURE.md                    # Detailed architecture documentation
├── .env.example                       # Environment variables template
├── requirements.txt                   # Python dependencies
├── backend/
│   ├── main.py                       # FastAPI application entry point
│   ├── api/
│   │   ├── chat.py                   # API routes
│   │   └── calendly_integration.py   # Core scheduling logic
│   ├── tools/
│   │   ├── availability_tool.py      # Availability utilities
│   │   └── booking_tool.py           # Booking utilities
│   └── models/
│       └── schemas.py                # Pydantic models
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.jsx
│       ├── components/
│       │   ├── AppointmentScheduler.jsx
│       │   ├── AvailabilityChecker.jsx
│       │   ├── BookingForm.jsx
│       │   └── ConfirmationModal.jsx
│       └── index.js
├── data/
│   ├── clinic_info.json              # Clinic information & FAQs
│   └── doctor_schedule.json          # Doctor schedules
└── tests/
    └── test_agent.py                 # Comprehensive test suite
```

## Example Usage

### Using cURL

**Check availability:**
```bash
curl "http://127.0.0.1:8000/api/calendly/availability?date=2025-11-21&appointment_type=consultation"
```

**Book appointment:**
```bash
curl -X POST "http://127.0.0.1:8000/api/calendly/book" \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_type": "consultation",
    "date": "2025-11-21",
    "start_time": "10:00",
    "patient": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-1234"
    },
    "reason": "Routine checkup"
  }'
```

### Using Postman

1. Import the API endpoints into Postman
2. Set up environment variables for base URL
3. Test each endpoint with provided examples

## Frontend Features

- **Multi-step booking flow**: Appointment type → Availability → Patient info → Confirmation
- **Real-time validation**: Form validation with helpful error messages
- **Responsive design**: Works on desktop and mobile devices
- **Beautiful UI**: Modern gradient design with smooth animations
- **Error handling**: User-friendly error messages and recovery options

## Deployment

### Backend Deployment

The FastAPI backend can be deployed to:
- Heroku
- AWS Lambda
- Google Cloud Run
- DigitalOcean
- Railway

### Frontend Deployment

The React frontend can be deployed to:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

## Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Available variables:
- `DEBUG`: Enable debug mode
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `BUSINESS_START_HOUR`: Clinic opening hour (default: 9)
- `BUSINESS_END_HOUR`: Clinic closing hour (default: 17)

## Workflow

1. **User selects appointment type** → Frontend shows appointment type options
2. **User picks date** → Backend generates available slots
3. **User selects time slot** → Frontend displays selected slot
4. **User enters details** → Frontend validates patient information
5. **User confirms booking** → Backend creates booking and returns confirmation
6. **Confirmation displayed** → User receives booking ID and confirmation code

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 400 Bad Request | Invalid appointment type | Use one of: consultation, followup, physical, specialist |
| 400 Bad Request | Invalid date format | Use YYYY-MM-DD format |
| 400 Bad Request | Past date | Select a future date |
| 409 Conflict | Slot no longer available | Select another available slot |
| 422 Validation Error | Missing patient info | Fill in all required fields |

## Security Considerations

- CORS enabled for frontend communication
- Input validation on all endpoints
- No sensitive data stored in-memory (use database in production)
- Form validation prevents invalid data submission

## Documentation

- **Architecture**: See `ARCHITECTURE.md` for detailed system design
- **API Docs**: Available at `http://127.0.0.1:8000/docs` (Swagger UI)
- **Tests**: See `tests/test_agent.py` for comprehensive examples

## Learning Resources

This implementation demonstrates:
- FastAPI best practices
- React hooks and state management
- RESTful API design
- Form validation patterns
- Error handling strategies
- Testing with pytest
- Component-based architecture

## Contributing

Contributions are welcome! Areas for enhancement:
- Real Calendly API integration
- Database persistence
- RAG/FAQ system
- Conversational agent
- Multi-language support
- Timezone handling

## License

This project is provided as-is for educational purposes.

## Troubleshooting

**Port already in use:**
```bash
# Change port in backend/main.py or use:
uvicorn backend.main:app --port 8002
```

**Frontend can't connect to backend:**
- Ensure backend is running on port 8000
- Check CORS settings in backend/main.py
- Verify API_BASE_URL in frontend/src/components/AppointmentScheduler.jsx

**Tests failing:**
```bash
# Run with verbose output:
pytest tests/ -v -s
```

## Support

For issues or questions:
1. Check the ARCHITECTURE.md documentation
2. Review test cases in tests/test_agent.py
3. Check API documentation at /docs endpoint
