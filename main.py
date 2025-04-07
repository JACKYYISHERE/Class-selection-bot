from models import Course
from recommender import ClassRecommender
from chat_interface import ChatInterface
from datetime import time

def create_sample_courses():
    """Create a sample set of courses for demonstration"""
    return [
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

def main():
    # Create sample courses
    courses = create_sample_courses()
    
    # Initialize the recommender
    recommender = ClassRecommender(courses)
    
    # Initialize the chat interface
    chat_interface = ChatInterface()
    
    print("Welcome to the AI Class Selection Assistant!")
    print("You can tell me your preferences in natural language, and I'll help you find the best classes.")
    print("For example, you can say: 'I prefer morning classes on Monday and Wednesday, with a maximum of 2 classes per day.'")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("What are your preferences for this semester? ")
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        preferences, questions = chat_interface.chat(user_input)
        
        if questions:
            print("\nI need some more information:")
            for question in questions:
                print(f"- {question}")
            continue
            
        if not preferences:
            print("I'm sorry, I couldn't understand your preferences. Please try again.")
            continue
            
        required_credits = int(input("\nHow many credits do you need to take? "))
        
        recommendations = recommender.recommend_courses(preferences, required_credits)
        
        if recommendations:
            print("\nBased on your preferences, here are the recommended courses:")
            for course in recommendations:
                print(f"\n{course.course_name} ({course.course_id})")
                print(f"Time: {course.time_slot.strftime('%I:%M %p')}")
                print(f"Days: {', '.join(course.days)}")
                print(f"Location: {course.building} {course.room}")
                print(f"Professor: {course.professor}")
                print(f"Credits: {course.credits}")
                print(f"Availability: {course.capacity - course.enrolled}/{course.capacity}")
        else:
            print("\nI couldn't find any courses that match your preferences. Would you like to try different preferences?")

if __name__ == "__main__":
    main() 