import React from 'react';
import './ConfirmationModal.css';

const ConfirmationModal = ({ confirmation, onNewBooking }) => {
  const formatDate = (dateStr) => {
    return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="confirmation-modal">
      <div className="confirmation-content">
        <div className="success-icon">✓</div>
        <h2>Appointment Confirmed!</h2>
        <p className="confirmation-message">
          Your appointment has been successfully booked.
        </p>

        <div className="confirmation-details">
          <div className="detail-section">
            <h3>Booking Details</h3>
            <div className="detail-item">
              <span className="detail-label">Confirmation Code:</span>
              <span className="detail-value code">{confirmation.confirmation_code}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Booking ID:</span>
              <span className="detail-value">{confirmation.booking_id}</span>
            </div>
          </div>

          <div className="detail-section">
            <h3>Appointment Information</h3>
            <div className="detail-item">
              <span className="detail-label">Type:</span>
              <span className="detail-value">
                {confirmation.details.appointment_type.charAt(0).toUpperCase() +
                  confirmation.details.appointment_type.slice(1)}
              </span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Date:</span>
              <span className="detail-value">
                {formatDate(confirmation.details.date)}
              </span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Time:</span>
              <span className="detail-value">
                {confirmation.details.start_time} - {confirmation.details.end_time}
              </span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Duration:</span>
              <span className="detail-value">
                {confirmation.details.duration_minutes} minutes
              </span>
            </div>
            {confirmation.details.reason && (
              <div className="detail-item">
                <span className="detail-label">Reason:</span>
                <span className="detail-value">{confirmation.details.reason}</span>
              </div>
            )}
          </div>

          <div className="detail-section">
            <h3>Patient Information</h3>
            <div className="detail-item">
              <span className="detail-label">Name:</span>
              <span className="detail-value">{confirmation.details.patient.name}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Email:</span>
              <span className="detail-value">{confirmation.details.patient.email}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Phone:</span>
              <span className="detail-value">{confirmation.details.patient.phone}</span>
            </div>
          </div>
        </div>

        <div className="confirmation-footer">
          <p>A confirmation email has been sent to {confirmation.details.patient.email}</p>
          <button className="new-booking-btn" onClick={onNewBooking}>
            Book Another Appointment
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationModal;
