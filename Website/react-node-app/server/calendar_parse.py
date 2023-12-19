from ics import Calendar
import requests
 
# Parse the URL
url = "https://calendar.google.com/calendar/u/0/embed?src=ccesportslab1@gmail.com&ctz=America/Denver&pli=1"
cal = Calendar(requests.get(url).text)
 
# Print all the events
print(cal.events)
