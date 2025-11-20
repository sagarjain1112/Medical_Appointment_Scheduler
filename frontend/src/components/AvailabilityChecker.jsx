import React, { useState } from 'react';
import './AvailabilityChecker.css';

const AvailabilityChecker = ({
  appointmentType,
  selectedDate,
  availableSlots,
  loading,
  onCheckAvailability,
  onSlotSelect,
  onBack,
}) => {
  const [inputDate, setInputDate] = useState(selectedDate || '');

  const handleDateChange = (e) => {
    setInputDate(e.target.value);
  };

  const handleCheckAvailability = () => {
    if (inputDate) {
      onCheckAvailability(inputDate);
    }
  };

  const getTodayDate = () => {
    const today = new Date();
    return today.toISOString().split('T')[0];
  };

  return (
    <div className="availability-checker">
      <div className="step-header">
        <button className="back-btn" onClick={onBack}>
          ← Back
        </button>
        <h2>Select Date & Time</h2>
      </div>

      <div className="date-selector">
        <label>Select Date:</label>
        <input
          type="date"
          value={inputDate}
          onChange={handleDateChange}
          min={getTodayDate()}
        />
        <button
          className="check-btn"
          onClick={handleCheckAvailability}
          disabled={!inputDate || loading}
        >
          {loading ? 'Checking...' : 'Check Availability'}
        </button>
      </div>

      {selectedDate && (
        <div className="appointment-info">
          <p>
            <strong>Type:</strong> {appointmentType.label}
          </p>
          <p>
            <strong>Duration:</strong> {appointmentType.duration}
          </p>
          <p>
            <strong>Date:</strong> {new Date(selectedDate + 'T00:00:00').toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </p>
        </div>
      )}

      {availableSlots.length > 0 && (
        <div className="slots-container">
          <h3>Available Time Slots</h3>
          <div className="slots-grid">
            {availableSlots.map((slot, index) => (
              <button
                key={index}
                className={`slot-btn ${slot.available ? 'available' : 'booked'}`}
                onClick={() => slot.available && onSlotSelect(slot)}
                disabled={!slot.available}
              >
                <div className="slot-time">
                  {slot.start_time} - {slot.end_time}
                </div>
                <div className="slot-status">
                  {slot.available ? '✓ Available' : '✗ Booked'}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {selectedDate && availableSlots.length === 0 && !loading && (
        <div className="no-slots">
          <p>No available slots for this date.</p>
          <p>Please try another date.</p>
        </div>
      )}
    </div>
  );
};

export default AvailabilityChecker;
