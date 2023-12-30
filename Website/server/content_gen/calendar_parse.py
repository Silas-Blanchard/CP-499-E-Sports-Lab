from ics import Calendar
import requests
from datetime import datetime, timedelta

def is_event_today(event, today):
    # Check if the event is for today
    return event.begin.date() == today

def is_event_tomorrow(event, tomorrow):
    # Check if the event is for tomorrow
    return event.begin.date() == tomorrow

# URL of the iCalendar
url = "https://calendar.google.com/calendar/ical/ccesportslab1%40gmail.com/public/basic.ics"
try:
    # Attempt to fetch the calendar data
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    cal = Calendar(response.text)
except requests.RequestException as e:
    print(f"Error fetching calendar data: {e}")
    exit()

# Today and tomorrow's dates
today = datetime.now().date()
tomorrow = today + timedelta(days=1)

# Print out all events in the calendar
#print("All Events in Calendar:")
#for event in cal.events:
#    print(f"Event: {event.name}, Starts: {event.begin.format('YYYY-MM-DD HH:mm')}")

# Filter events for today and tomorrow using list comprehensions
events_today = [event for event in cal.events if is_event_today(event, today)]
events_tomorrow = [event for event in cal.events if is_event_tomorrow(event, tomorrow)]

# Output for today's events
if events_today:
    for event in events_today:
        print(f"Today: {event.name} at {event.begin.format('YYYY-MM-DD HH:mm')}")
else:
    print("No events today")

# Output for tomorrow's events
if events_tomorrow:
    for event in events_tomorrow:
        print(f"Tomorrow: {event.name} at {event.begin.format('YYYY-MM-DD HH:mm')}")
else:
    print("No events tomorrow")
