import os
from openai import OpenAI
from dotenv import load_dotenv
from models import StudentPreferences
from datetime import time
import json

class ChatInterface:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompt = """You are a helpful class selection assistant. Your task is to extract student preferences 
        from their natural language input and convert them into structured data. You should ask clarifying questions 
        when needed and ensure all necessary information is collected.

        The preferences you need to collect are:
        1. Maximum commute time (in minutes)
        2. Preferred class times (in 24-hour format)
        3. Preferred days of the week
        4. Maximum number of classes per day
        5. Minimum gap between classes (in minutes)
        6. Preferred subjects
        7. Preferred campus (optional)
        8. Required number of credits

        Format your response as a JSON object with these fields. If any information is missing, ask for it.
        """

    def parse_time(self, time_str: str) -> time:
        """Convert time string to time object"""
        try:
            hour, minute = map(int, time_str.split(':'))
            return time(hour, minute)
        except ValueError:
            return None

    def extract_preferences(self, user_input: str) -> dict:
        """Extract preferences from user input using ChatGPT"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ],
            response_format={"type": "json_object"}
        )
        
        try:
            preferences = json.loads(response.choices[0].message.content)
            return preferences
        except json.JSONDecodeError:
            return None

    def convert_to_student_preferences(self, preferences_dict: dict) -> StudentPreferences:
        """Convert the extracted preferences into a StudentPreferences object"""
        return StudentPreferences(
            max_commute_time=int(preferences_dict.get('max_commute_time', 0)),
            preferred_time_slots=[self.parse_time(t) for t in preferences_dict.get('preferred_time_slots', [])],
            preferred_days=preferences_dict.get('preferred_days', []),
            max_classes_per_day=int(preferences_dict.get('max_classes_per_day', 0)),
            preferred_subjects=preferences_dict.get('preferred_subjects', []),
            min_gap_between_classes=int(preferences_dict.get('min_gap_between_classes', 0)),
            preferred_campus=preferences_dict.get('preferred_campus', None)
        )

    def get_clarifying_questions(self, preferences_dict: dict) -> list:
        """Generate questions for missing or unclear preferences"""
        questions = []
        if not preferences_dict.get('max_commute_time'):
            questions.append("What is your maximum acceptable commute time in minutes?")
        if not preferences_dict.get('preferred_time_slots'):
            questions.append("What are your preferred class times? (e.g., 9:00 AM, 2:00 PM)")
        if not preferences_dict.get('preferred_days'):
            questions.append("Which days of the week do you prefer for classes?")
        if not preferences_dict.get('max_classes_per_day'):
            questions.append("What is the maximum number of classes you want to take per day?")
        if not preferences_dict.get('min_gap_between_classes'):
            questions.append("What is the minimum gap you want between classes in minutes?")
        if not preferences_dict.get('preferred_subjects'):
            questions.append("What subjects are you interested in?")
        return questions

    def chat(self, user_input: str) -> tuple[StudentPreferences, list]:
        """Main chat interface that handles the conversation"""
        preferences_dict = self.extract_preferences(user_input)
        if not preferences_dict:
            return None, ["I'm sorry, I couldn't understand your preferences. Could you please try again?"]
        
        clarifying_questions = self.get_clarifying_questions(preferences_dict)
        if clarifying_questions:
            return None, clarifying_questions
        
        try:
            preferences = self.convert_to_student_preferences(preferences_dict)
            return preferences, []
        except (ValueError, TypeError) as e:
            return None, [f"I encountered an error processing your preferences: {str(e)}. Could you please clarify?"] 