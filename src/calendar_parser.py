import requests
from icalendar import Calendar
from datetime import datetime
from urllib.parse import urlparse, urlunparse

def parse_calendar_url(url):
    if url.startswith("webcal://"):
        url = "http://" + url[9:]
    response = requests.get(url)
    print(Calendar.from_ical(response.content))
    return Calendar.from_ical(response.content)

def make_naive(dt):
    """Convert datetime to naive by removing timezone info."""
    return dt.replace(tzinfo=None) if dt.tzinfo else dt

def get_events(calendar, start_date, end_date):
    events = []
    # print(f"start date: {start_date} - end data: {end_date}")
    for component in calendar.walk('VEVENT'):
        event_start = make_naive(component.get('dtstart').dt)
        event_end = make_naive(component.get('dtend').dt)
        summary = component.get('summary')
        # print(f"event start date: {event_start} - event end data: {event_end}")

        if not (event_end.date() < start_date or event_start.date() > end_date):
            events.append({
                'start': event_start,
                'end': event_end,
                'summary': summary
            })
    return events