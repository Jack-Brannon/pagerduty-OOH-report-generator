from datetime import datetime, time, timedelta
from config import (
    BANK_HOLIDAYS,
    DATE_FORMAT,
    WORKDAY_START,
    WORKDAY_END,
)

def parse_time_string(time_str):
    """Conver time string (HH:MM) to a datetime.time object."""
    hours, minutes = map(int, time_str.split(":"))
    return time(hours, minutes)

# Prase workday start and end times
WORKDAY_START_TIME = parse_time_string(WORKDAY_START)
WORKDAY_END_TIME = parse_time_string(WORKDAY_END)

def is_weekend(date):
    """Check if date is a Saturday or Sunday."""
    return date.weekday() in [5,6]

def is_bank_holiday(date):
    """Check if a date is a bank holiday."""
    return date.strftime(DATE_FORMAT) in BANK_HOLIDAYS

def classify_shift_segemnt(start, end):
    """Classify a single shift segment."""
    start = start.replace(tzinfo=None)
    end = end.replace(tzinfo=None)
    
    segments = []
    current_date = start.date()

    while start < end:
        print(f"Processing: {start}")
        if is_bank_holiday(current_date):
            category = "Bank Holiday"
            next_boundary = datetime.combine(current_date + timedelta(days=1), WORKDAY_START_TIME)
        
        elif current_date.weekday() >= 5:  # Weekend
            category = "Weekend"
            next_boundary = datetime.combine(current_date + timedelta(days=1), WORKDAY_START_TIME)
        
        else:  # Weekday
            if start.time() >= WORKDAY_END_TIME:
                category = "Weekday"
                next_boundary = datetime.combine(current_date + timedelta(days=1), WORKDAY_START_TIME)
            else:
                # Skip working hours
                start = datetime.combine(current_date, WORKDAY_END_TIME)
                current_date = start.date()
                continue

        segment_end = min(next_boundary, end)
       
        if segment_end > start:
            segments.append({   
                "start": start,
                "end": segment_end,
                "category": category
            })

        start = segment_end
        current_date = start.date()

    return segments

def classify_shifts(events):
    """Classify and segment all shifts."""
    classified_shifts = []

    for event in events:
        start = event['start']
        end = event['end']
        user = event['summary']

        segments = classify_shift_segemnt(start, end)
        for segment in segments:
            classified_shifts.append({
                "user": user,
                "start": segment['start'],
                "end": segment['end'],
                "category": segment['category']
            })
    
    return classified_shifts
