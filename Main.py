from CoursesTree import CoursesTree
from Student import Student

student = None
while student == None:
    username = input("Enter username: ")
    password = input("Enter password: ")
    print("\nLOADING...")
    try:
        student = Student(username, password)
    except Exception as e:
        print(e)
        print("Username or Password is wrong!")

coursesTree = CoursesTree(student)
