from ics import Calendar
import requests
 
# Parse the URL
url = "https://calendar.google.com/calendar/ical/ht3jlfaac5lfd6263ulfh4tql8%40group.calendar.google.com/public/basic.ics"
cal = Calendar(requests.get(url).text)
 
# Print all the events
print(cal.events)
