import React, { useState } from 'react';
import axios from 'axios';
import './AppointmentScheduler.css';
import AvailabilityChecker from './AvailabilityChecker';
import BookingForm from './BookingForm';
import ConfirmationModal from './ConfirmationModal';

const API_BASE_URL = 'http://127.0.0.1:8000';

const AppointmentScheduler = () => {
  const [currentStep, setCurrentStep] = useState('appointment-type'); // appointment-type, availability, booking, confirmation
  const [appointmentType, setAppointmentType] = useState('');
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedSlot, setSelectedSlot] = useState('');
  const [availableSlots, setAvailableSlots] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [bookingConfirmation, setBookingConfirmation] = useState(null);

  const appointmentTypes = {
    consultation: { label: 'General Consultation', duration: '30 minutes' },
    followup: { label: 'Follow-up', duration: '15 minutes' },
    physical: { label: 'Physical Exam', duration: '45 minutes' },
    specialist: { label: 'Specialist Consultation', duration: '60 minutes' },
  };

  const handleAppointmentTypeSelect = (type) => {
    setAppointmentType(type);
    setCurrentStep('availability');
    setError('');
  };

  const handleCheckAvailability = async (date) => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`${API_BASE_URL}/api/calendly/availability`, {
        params: {
          date: date,
          appointment_type: appointmentType,
        },
      });
      setAvailableSlots(response.data.available_slots);
      setSelectedDate(date);
      if (response.data.available_slots.length === 0) {
        setError('No available slots for this date. Please try another date.');
      }
    } catch (err) {
      setError('Failed to fetch availability. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSlotSelect = (slot) => {
    setSelectedSlot(slot);
    setCurrentStep('booking');
  };

  const handleBookingSubmit = async (patientInfo) => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.post(`${API_BASE_URL}/api/calendly/book`, {
        appointment_type: appointmentType,
        date: selectedDate,
        start_time: selectedSlot.start_time,
        patient: patientInfo,
        reason: patientInfo.reason,
      });
      setBookingConfirmation(response.data);
      setCurrentStep('confirmation');
    } catch (err) {
      if (err.response?.status === 409) {
        setError('This slot is no longer available. Please select another slot.');
        setCurrentStep('availability');
      } else {
        setError('Failed to book appointment. Please try again.');
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleNewBooking = () => {
    setCurrentStep('appointment-type');
    setAppointmentType('');
    setSelectedDate('');
    setSelectedSlot('');
    setAvailableSlots([]);
    setError('');
    setBookingConfirmation(null);
  };

  const handleBackStep = () => {
    if (currentStep === 'booking') {
      setCurrentStep('availability');
      setSelectedSlot('');
    } else if (currentStep === 'availability') {
      setCurrentStep('appointment-type');
      setAppointmentType('');
    }
  };

  return (
    <div className="scheduler-container">
      <div className="scheduler-card">
        <div className="scheduler-header">
          <h1>Medical Appointment Scheduler</h1>
          <p>Book your appointment in just a few steps</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        {currentStep === 'appointment-type' && (
          <div className="step-content">
            <h2>Select Appointment Type</h2>
            <div className="appointment-types">
              {Object.entries(appointmentTypes).map(([key, value]) => (
                <button
                  key={key}
                  className="appointment-type-btn"
                  onClick={() => handleAppointmentTypeSelect(key)}
                >
                  <div className="type-label">{value.label}</div>
                  <div className="type-duration">{value.duration}</div>
                </button>
              ))}
            </div>
          </div>
        )}

        {currentStep === 'availability' && (
          <AvailabilityChecker
            appointmentType={appointmentTypes[appointmentType]}
            selectedDate={selectedDate}
            availableSlots={availableSlots}
            loading={loading}
            onCheckAvailability={handleCheckAvailability}
            onSlotSelect={handleSlotSelect}
            onBack={handleBackStep}
          />
        )}

        {currentStep === 'booking' && (
          <BookingForm
            appointmentType={appointmentTypes[appointmentType]}
            selectedDate={selectedDate}
            selectedSlot={selectedSlot}
            loading={loading}
            onSubmit={handleBookingSubmit}
            onBack={handleBackStep}
          />
        )}

        {currentStep === 'confirmation' && (
          <ConfirmationModal
            confirmation={bookingConfirmation}
            onNewBooking={handleNewBooking}
          />
        )}
      </div>
    </div>
  );
};

export default AppointmentScheduler;
