import re
from collections import deque
def printSet(coursesSet, title):
    print("##############################")
    print(title)
    count = 1
    if len(coursesSet) == 0:
        print("\tNo Courses Available!")
    else:
        for course in coursesSet:
            print("\t", course.getName(),"- ", count)
            count+=1
    print("##############################")

counter = 0
def dfs(course,level):
    global counter
    if course is None:
        return
    if course.getIsOptional():
        counter += level
    else:
        counter += level + 1
    for child in course.getChildrenSet():
        dfs(child,level+1)

def anyYear(course):
    if course.getNotes().__contains__("السنة - 1"):
        return 3
    elif course.getNotes().__contains__("السنة - 2"):
        return 2
    elif course.getNotes().__contains__("السنة - 3"):
        return 1
    else:
        return 0

def setRank(availableCourses,student):
    global counter
    optionalCommon = set()
    obligatoryCommon = set()
    optionalDegree = set()
    labs = set()
    rest = set()

    for course in availableCourses:
        dfs(course,0)
        course.setRank(course.getRank() + counter + anyYear(course))
        counter = 0

    for course in availableCourses:
        if course in student.getOptionalCommonSet():
            optionalCommon.add(course)
        elif course in student.getOptionalDegreeSet():
            optionalDegree.add(course)
        elif course in student.getObligatoryCommonSet():
            obligatoryCommon.add(course)
        elif course in student.getObligatoryDegreeSet() or course in student.getObligatoryCollageSet():
            if course.getNumberOfHours() == 1:
                labs.add(course)
            else:
                rest.add(course)

    optionalCommon = sorted(optionalCommon, key=lambda course: course.getRank(), reverse=True)
    obligatoryCommon = sorted(obligatoryCommon, key=lambda course: course.getRank(), reverse=True)
    optionalDegree = sorted(optionalDegree, key=lambda course: course.getRank(), reverse=True)
    labs = sorted(labs, key=lambda course: course.getRank(), reverse=True)
    rest = sorted(rest, key=lambda course: course.getRank(), reverse=True)

    printSet(rest,"1- Degree Courses: ")
    printSet(labs, "2- Degree Labs: ")
    printSet(optionalDegree, "3- Optional Degree Courses: ")
    printSet(obligatoryCommon, "4- Obligatory Common Courses: ")
    printSet(optionalCommon,"5- Optional Common Courses: ")



