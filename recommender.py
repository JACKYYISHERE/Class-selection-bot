from typing import List, Dict
from datetime import time, datetime
from models import StudentPreferences, Course, Schedule
import numpy as np

class ClassRecommender:
    def __init__(self, available_courses: List[Course]):
        self.available_courses = available_courses

    def calculate_course_score(self, course: Course, preferences: StudentPreferences) -> float:
        """Calculate a score for a course based on student preferences"""
        score = 0.0
        
        # Time slot preference
        if course.time_slot in preferences.preferred_time_slots:
            score += 2.0
        
        # Day preference
        for day in course.days:
            if day in preferences.preferred_days:
                score += 1.0
        
        # Subject preference
        if course.subject in preferences.preferred_subjects:
            score += 3.0
        
        # Campus preference
        if preferences.preferred_campus and course.campus == preferences.preferred_campus:
            score += 2.0
        
        # Class capacity (prefer classes with more available spots)
        availability_ratio = (course.capacity - course.enrolled) / course.capacity
        score += availability_ratio * 2.0
        
        return score

    def check_schedule_conflicts(self, schedule: Schedule, new_course: Course) -> bool:
        """Check if adding a new course would create conflicts with existing schedule"""
        for existing_course in schedule.courses:
            # Check day conflicts
            if any(day in existing_course.days for day in new_course.days):
                # Check time conflicts
                existing_start = datetime.combine(datetime.today(), existing_course.time_slot)
                new_start = datetime.combine(datetime.today(), new_course.time_slot)
                
                # Assuming each class is 1 hour long
                existing_end = existing_start.replace(hour=existing_start.hour + 1)
                new_end = new_start.replace(hour=new_start.hour + 1)
                
                if (new_start < existing_end and new_end > existing_start):
                    return True
        return False

    def recommend_courses(self, preferences: StudentPreferences, required_credits: int) -> List[Course]:
        """Generate course recommendations based on student preferences"""
        recommended_courses = []
        current_schedule = Schedule(
            student_id="temp",
            courses=[],
            total_credits=0,
            commute_time=0
        )
        
        # Sort courses by score
        scored_courses = [
            (course, self.calculate_course_score(course, preferences))
            for course in self.available_courses
        ]
        scored_courses.sort(key=lambda x: x[1], reverse=True)
        
        for course, score in scored_courses:
            if current_schedule.total_credits >= required_credits:
                break
                
            # Check if adding this course would exceed daily class limit
            daily_classes = {}
            for c in current_schedule.courses + [course]:
                for day in c.days:
                    daily_classes[day] = daily_classes.get(day, 0) + 1
                    if daily_classes[day] > preferences.max_classes_per_day:
                        continue
            
            # Check for schedule conflicts
            if not self.check_schedule_conflicts(current_schedule, course):
                recommended_courses.append(course)
                current_schedule.courses.append(course)
                current_schedule.total_credits += course.credits
        
        return recommended_courses

    def get_schedule_summary(self, schedule: Schedule) -> Dict:
        """Generate a summary of the recommended schedule"""
        return {
            "total_credits": schedule.total_credits,
            "courses": [
                {
                    "course_id": course.course_id,
                    "course_name": course.course_name,
                    "time": course.time_slot.strftime("%I:%M %p"),
                    "days": course.days,
                    "location": f"{course.building} {course.room}"
                }
                for course in schedule.courses
            ],
            "daily_schedule": self._generate_daily_schedule(schedule)
        }

    def _generate_daily_schedule(self, schedule: Schedule) -> Dict:
        """Generate a daily schedule view"""
        daily_schedule = {}
        for course in schedule.courses:
            for day in course.days:
                if day not in daily_schedule:
                    daily_schedule[day] = []
                daily_schedule[day].append({
                    "course": course.course_name,
                    "time": course.time_slot.strftime("%I:%M %p"),
                    "location": f"{course.building} {course.room}"
                })
        return daily_schedule 