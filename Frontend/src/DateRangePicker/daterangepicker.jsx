import React, { useState } from 'react';
import '../Hero/hero.css';
import '../tripcreator/createTrip2.css';

function DateRangePicker({ onDateRangeSelected }) {
    const [selectedStartDate, setSelectedStartDate] = useState(null);
    const [selectedEndDate, setSelectedEndDate] = useState(null);
    const [currentMonth, setCurrentMonth] = useState(new Date().getMonth());
    const [currentYear, setCurrentYear] = useState(new Date().getFullYear());

    const daysInMonth = (month, year) => {
        return new Date(year, month + 1, 0).getDate();
    };

    const handleDayClick = (day) => {
        const date = new Date(currentYear, currentMonth, day);
        if (!selectedStartDate || (selectedStartDate && selectedEndDate)) {
            setSelectedStartDate(date);
            setSelectedEndDate(null);
        } else if (selectedStartDate && !selectedEndDate) {
            if (date >= selectedStartDate) {
                setSelectedEndDate(date);
                onDateRangeSelected({ start: selectedStartDate, end: date });
            } else {
                setSelectedStartDate(date);
            }
        }
    };

    const renderDays = () => {
        const days = [];
        const daysInCurrentMonth = daysInMonth(currentMonth, currentYear);
        for (let i = 1; i <= daysInCurrentMonth; i++) {
            const date = new Date(currentYear, currentMonth, i);
            const isSelectedStart = selectedStartDate && date.toDateString() === selectedStartDate.toDateString();
            const isSelectedEnd = selectedEndDate && date.toDateString() === selectedEndDate.toDateString();
            const isInRange = selectedStartDate && selectedEndDate && date > selectedStartDate && date < selectedEndDate;
            days.push(
                <div
                    key={i}
                    className={`day ${isSelectedStart ? 'selected-start' : ''} ${isSelectedEnd ? 'selected-end' : ''} ${isInRange ? 'in-range' : ''}`}
                    onClick={() => handleDayClick(i)}
                >
                    {i}
                </div>
            );
        }
        return days;
    };

    const handleMonthChange = (direction) => {
        if (direction === 'prev') {
            if (currentMonth === 0) {
                setCurrentMonth(11);
                setCurrentYear(currentYear - 1);
            } else {
                setCurrentMonth(currentMonth - 1);
            }
        } else if (direction === 'next') {
            if (currentMonth === 11) {
                setCurrentMonth(0);
                setCurrentYear(currentYear + 1);
            } else {
                setCurrentMonth(currentMonth + 1);
            }
        }
    };

    return (
        <div className="calendar">
            <div className="calendar-header">
                <a onClick={() => handleMonthChange('prev')}>Previous</a>
                <span>{`${currentYear} - ${currentMonth + 1}`}</span>
                <a onClick={() => handleMonthChange('next')}>Next</a>
            </div>
            <div className="calendar-body">
                {renderDays()}
            </div>
        </div>
    );
}

export default DateRangePicker;
