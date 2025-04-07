from dataclasses import dataclass
from typing import List, Optional
from datetime import time

@dataclass
class StudentPreferences:
    """Represents a student's preferences for class selection"""
    max_commute_time: int  # in minutes
    preferred_time_slots: List[time]  # preferred class times
    preferred_days: List[str]  # e.g., ['Monday', 'Wednesday']
    max_classes_per_day: int
    preferred_subjects: List[str]
    min_gap_between_classes: int  # in minutes
    preferred_campus: Optional[str] = None

@dataclass
class Course:
    """Represents a course offering"""
    course_id: str
    course_name: str
    subject: str
    credits: int
    professor: str
    time_slot: time
    days: List[str]
    campus: str
    building: str
    room: str
    capacity: int
    enrolled: int = 0

@dataclass
class Schedule:
    """Represents a student's class schedule"""
    student_id: str
    courses: List[Course]
    total_credits: int
    commute_time: int  # in minutes 