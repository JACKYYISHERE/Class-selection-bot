import streamlit as st
from models import Course
from recommender import ClassRecommender
from chat_interface import ChatInterface
from datetime import time

# Initialize components
courses = [
    Course(
        course_id="CS101",
        course_name="Introduction to Computer Science",
        subject="Computer Science",
        credits=3,
        professor="Dr. Smith",
        time_slot=time(9, 0),
        days=["Monday", "Wednesday"],
        campus="Main Campus",
        building="Science Hall",
        room="101",
        capacity=30,
        enrolled=15
    ),
    Course(
        course_id="MATH201",
        course_name="Calculus II",
        subject="Mathematics",
        credits=4,
        professor="Dr. Johnson",
        time_slot=time(11, 0),
        days=["Tuesday", "Thursday"],
        campus="Main Campus",
        building="Math Building",
        room="205",
        capacity=25,
        enrolled=20
    ),
    Course(
        course_id="ENG101",
        course_name="English Composition",
        subject="English",
        credits=3,
        professor="Dr. Williams",
        time_slot=time(14, 0),
        days=["Monday", "Wednesday", "Friday"],
        campus="Main Campus",
        building="Humanities Hall",
        room="301",
        capacity=35,
        enrolled=25
    ),
    Course(
        course_id="PHYS101",
        course_name="Physics I",
        subject="Physics",
        credits=4,
        professor="Dr. Brown",
        time_slot=time(10, 0),
        days=["Tuesday", "Thursday"],
        campus="Science Campus",
        building="Physics Building",
        room="102",
        capacity=30,
        enrolled=18
    ),
    Course(
        course_id="HIST101",
        course_name="World History",
        subject="History",
        credits=3,
        professor="Dr. Davis",
        time_slot=time(13, 0),
        days=["Monday", "Wednesday"],
        campus="Main Campus",
        building="History Building",
        room="201",
        capacity=40,
        enrolled=30
    )
]

recommender = ClassRecommender(courses)
chat_interface = ChatInterface()

# Set page config
st.set_page_config(
    page_title="AI Class Selection Assistant",
    page_icon="🎓",
    layout="wide"
)

# Title and description
st.title("🎓 AI Class Selection Assistant")
st.markdown("""
Tell me your preferences in natural language. For example:
- "I want morning classes on Monday and Wednesday"
- "I prefer computer science and math classes"
- "I need classes with at least 30 minutes between them"
- "I can commute up to 20 minutes"
""")

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    preferences = st.text_area("Enter your preferences:", height=100)
with col2:
    required_credits = st.number_input("Required Credits:", min_value=1, max_value=24, value=12)

if st.button("Get Recommendations"):
    if preferences:
        # Get preferences from chat interface
        preferences_dict, questions = chat_interface.chat(preferences)
        
        if questions:
            st.warning("I need some more information:")
            for question in questions:
                st.write(question)
        elif not preferences_dict:
            st.error("I couldn't understand your preferences. Please try again.")
        else:
            # Get recommendations
            recommendations = recommender.recommend_courses(preferences_dict, required_credits)
            
            if recommendations:
                st.success("Here are your recommended courses:")
                for course in recommendations:
                    with st.expander(f"{course.course_name} ({course.course_id})"):
                        st.write(f"**Time:** {course.time_slot.strftime('%I:%M %p')}")
                        st.write(f"**Days:** {', '.join(course.days)}")
                        st.write(f"**Location:** {course.building} {course.room}")
                        st.write(f"**Professor:** {course.professor}")
                        st.write(f"**Credits:** {course.credits}")
                        st.write(f"**Availability:** {course.capacity - course.enrolled}/{course.capacity}")
            else:
                st.info("I couldn't find any courses that match your preferences.")
    else:
        st.warning("Please enter your preferences to get recommendations.") 