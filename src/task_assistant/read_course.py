
import json

def get_courses():
    with open("courses.json") as file:
        courses = json.load(file)
        #st.write(courses)
    return courses 

