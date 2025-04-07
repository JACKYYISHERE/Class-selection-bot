import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from models import Course

class CalendarManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.creds = None
        self.service = None
        self.initialize_service()

    def initialize_service(self):
        """Initialize the Google Calendar service with proper authentication"""
        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def create_calendar_event(self, course: Course, semester_start_date: str):
        """Create a calendar event for a course"""
        # Convert semester start date to datetime object
        start_date = datetime.strptime(semester_start_date, '%Y-%m-%d')
        
        # Find the first occurrence of each day in the course schedule
        events = []
        for day in course.days:
            # Convert day name to number (Monday = 0, Sunday = 6)
            day_num = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day)
            
            # Calculate the date of the first class
            days_to_add = (day_num - start_date.weekday()) % 7
            first_class_date = start_date + timedelta(days=days_to_add)
            
            # Create event for each week of the semester (assuming 16 weeks)
            for week in range(16):
                class_date = first_class_date + timedelta(weeks=week)
                
                # Create start and end times
                start_time = datetime.combine(class_date, course.time_slot)
                end_time = start_time + timedelta(hours=1)  # Assuming 1-hour classes
                
                event = {
                    'summary': f'{course.course_name} ({course.course_id})',
                    'location': f'{course.building} {course.room}',
                    'description': f'Professor: {course.professor}\nSubject: {course.subject}\nCredits: {course.credits}',
                    'start': {
                        'dateTime': start_time.isoformat(),
                        'timeZone': 'America/New_York',  # Adjust timezone as needed
                    },
                    'end': {
                        'dateTime': end_time.isoformat(),
                        'timeZone': 'America/New_York',
                    },
                    'recurrence': [],  # No recurrence as we're creating individual events
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'popup', 'minutes': 30},
                        ],
                    },
                }
                
                try:
                    event = self.service.events().insert(calendarId='primary', body=event).execute()
                    events.append(event)
                    print(f'Created event: {event.get("htmlLink")}')
                except Exception as e:
                    print(f'Error creating event: {e}')
        
        return events

    def add_schedule_to_calendar(self, courses: list[Course], semester_start_date: str):
        """Add all courses in a schedule to the calendar"""
        all_events = []
        for course in courses:
            events = self.create_calendar_event(course, semester_start_date)
            all_events.extend(events)
        return all_events 