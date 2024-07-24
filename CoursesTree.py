from collections import deque

import Rank
from Student import Student
from Rank import setRank
import re

def isItAllow(course,student):
    if "قد قطع" in course.getNotes():
        numberOfHoursBefore = int(re.search(r'\d\d', course.getNotes()).group())
        if student.getNumberOfCompletedHours() >= numberOfHoursBefore:
            return True
        else:
            return False
    else:
        return True

class CoursesTree:
    def __init__(self, student):
        self.__student = student
        self.__coursesSet = set()
        self.__coursesSet.update(self.__student.getObligatoryCommonSet(), self.__student.getOptionalCommonSet(),
                                 self.__student.getObligatoryCollageSet(), self.__student.getObligatoryDegreeSet(),
                                 self.__student.getOptionalDegreeSet())
        self.buildCoursesTree()
        self.__completedCourses = None
        self.__availableCourses = set()
        self.__bfs()
        Rank.setRank(self.__availableCourses,self.__student)

    def buildCoursesTree(self):
        for child in self.__coursesSet:
            for father in self.__coursesSet:
                if child.getNotes().__contains__(father.getName()):
                    father.addChild(child)
                    child.setFather(father)

    def __bfs(self):
        queue = deque()
        for course in self.__coursesSet:
            if not course.visited:
                if course.getFather() is None or course.getFather().getIsDone():
                    if isItAllow(course,self.__student):
                        queue.append(course)
                        course.visited = True
                        while queue:
                            currentCourse = queue.popleft()
                            if not currentCourse.getIsDone():
                                self.__availableCourses.add(currentCourse)
                            else:
                                for child in currentCourse.getChildrenSet():
                                    if not child.visited and isItAllow(currentCourse, self.__student):
                                            queue.append(child)
                                            child.visited = True
                elif course.getNumberOfHours() == 1 and course.getFather().getFather() is not None:
                    self.__availableCourses.add(course)

    def getAvailableCourses(self):
        return self.__availableCourses

