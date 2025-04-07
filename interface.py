from datetime import time
from models import StudentPreferences, Course
from recommender import ClassRecommender
import json

class ClassSelectorInterface:
    def __init__(self, recommender: ClassRecommender):
        self.recommender = recommender

    def collect_preferences(self) -> StudentPreferences:
        """Collect student preferences through a series of prompts"""
        print("\nWelcome to the Class Selection Assistant!")
        print("Please provide your preferences for the upcoming semester.\n")

        # Collect commute preferences
        max_commute = int(input("What is your maximum acceptable commute time (in minutes)? "))
        
        # Collect time preferences
        print("\nEnter your preferred class times (24-hour format, e.g., 09:00, 14:30)")
        print("Enter 'done' when finished")
        preferred_times = []
        while True:
            time_input = input("Preferred time (or 'done'): ")
            if time_input.lower() == 'done':
                break
            try:
                hour, minute = map(int, time_input.split(':'))
                preferred_times.append(time(hour, minute))
            except ValueError:
                print("Please enter time in HH:MM format")

        # Collect day preferences
        print("\nEnter your preferred days (e.g., Monday, Tuesday)")
        print("Enter 'done' when finished")
        preferred_days = []
        while True:
            day = input("Preferred day (or 'done'): ")
            if day.lower() == 'done':
                break
            preferred_days.append(day)

        # Collect other preferences
        max_classes = int(input("\nMaximum number of classes per day: "))
        min_gap = int(input("Minimum gap between classes (in minutes): "))
        
        print("\nEnter your preferred subjects")
        print("Enter 'done' when finished")
        preferred_subjects = []
        while True:
            subject = input("Preferred subject (or 'done'): ")
            if subject.lower() == 'done':
                break
            preferred_subjects.append(subject)

        campus = input("\nPreferred campus (optional, press Enter to skip): ")
        if not campus:
            campus = None

        return StudentPreferences(
            max_commute_time=max_commute,
            preferred_time_slots=preferred_times,
            preferred_days=preferred_days,
            max_classes_per_day=max_classes,
            preferred_subjects=preferred_subjects,
            min_gap_between_classes=min_gap,
            preferred_campus=campus
        )

    def display_recommendations(self, recommendations: list[Course]):
        """Display the recommended courses in a formatted way"""
        if not recommendations:
            print("\nNo suitable courses found based on your preferences.")
            return

        print("\nRecommended Courses:")
        print("-" * 80)
        for course in recommendations:
            print(f"\nCourse: {course.course_name} ({course.course_id})")
            print(f"Subject: {course.subject}")
            print(f"Professor: {course.professor}")
            print(f"Time: {course.time_slot.strftime('%I:%M %p')}")
            print(f"Days: {', '.join(course.days)}")
            print(f"Location: {course.building} {course.room}")
            print(f"Credits: {course.credits}")
            print(f"Availability: {course.capacity - course.enrolled}/{course.capacity}")
            print("-" * 80)

    def display_schedule_summary(self, summary: dict):
        """Display the schedule summary in a formatted way"""
        print("\nSchedule Summary:")
        print(f"Total Credits: {summary['total_credits']}")
        
        print("\nDaily Schedule:")
        for day, classes in summary['daily_schedule'].items():
            print(f"\n{day}:")
            for class_info in classes:
                print(f"  {class_info['time']} - {class_info['course']}")
                print(f"    Location: {class_info['location']}")

    def run(self):
        """Run the class selection interface"""
        preferences = self.collect_preferences()
        required_credits = int(input("\nHow many credits do you need to take? "))
        
        recommendations = self.recommender.recommend_courses(preferences, required_credits)
        self.display_recommendations(recommendations)
        
        if recommendations:
            schedule = self.recommender.get_schedule_summary(
                Schedule(
                    student_id="current",
                    courses=recommendations,
                    total_credits=sum(c.credits for c in recommendations),
                    commute_time=0  # This would be calculated based on actual locations
                )
            )
            self.display_schedule_summary(schedule) 