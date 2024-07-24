from Courses import Course
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep

numOfSet=0
def increaseNumOfSet():
    global numOfSet
    numOfSet+=1
def getNumOfSet():
    return numOfSet

class Student:
    def __init__(self, username, password):
        self.__numberOfCompletedHours = 0
        [self.__obligatoryCommonSet, self.__optionalCommonSet, self.__obligatoryCollageSet, self.__obligatoryDegreeSet,
         self.__optionalDegreeSet] = self.__getCourses(username, password)
    def __getCourses(self, username, password):
        obligatoryCommonSet = set()
        optionalCommonSet = set()

        obligatoryCollageSet = set()

        obligatoryDegreeSet = set()
        optionalDegreeSet = set()

        options = Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

        try:
            driver.get('https://application.bau.edu.jo/reg_new/index.jsp')
            sleep(0.5)

            driver.find_element(By.NAME, 'username').send_keys(username)
            password_field = driver.find_element(By.NAME, 'password')
            password_field.send_keys(password)
            sleep(0.5)

            password_field.send_keys(Keys.RETURN)
            sleep(2)

            driver.find_element(By.ID, 'navmenu').find_elements(By.TAG_NAME, 'li')[3].find_element(By.TAG_NAME,
                                                                                                   'a').click()
            sleep(1)

            for i in range(4, 20, 2):
                try:
                    table = driver.find_elements(By.TAG_NAME, 'table')[i]
                    for row in table.find_elements(By.TAG_NAME, 'tr'):
                        cells = row.find_elements(By.TAG_NAME, 'td')
                        cell_texts = [cell.text for cell in cells]

                        if cell_texts[0] == 'رقم المادة':
                            increaseNumOfSet()
                            continue
                        course = Course(cell_texts[0], cell_texts[1], cell_texts[2], cell_texts[3], cell_texts[4])

                        if int(course.getNumberOfHours()) > 0:
                            if getNumOfSet() == 1 or getNumOfSet() == 8:
                                obligatoryCommonSet.add(course)

                            elif getNumOfSet() == 2:
                                course.setIsOptional(True)
                                optionalCommonSet.add(course)

                            elif getNumOfSet() == 3:
                                obligatoryCollageSet.add(course)

                            elif getNumOfSet() == 4 or getNumOfSet() == 6:
                                obligatoryDegreeSet.add(course)

                            elif getNumOfSet() == 5:
                                course.setIsOptional(True)
                                optionalDegreeSet.add(course)
                            if course.getIsDone():
                                self.__numberOfCompletedHours += int(course.getNumberOfHours())
                except IndexError:
                    continue
        finally:
            driver.quit()
        return obligatoryCommonSet, optionalCommonSet, obligatoryCollageSet, obligatoryDegreeSet, optionalDegreeSet

    def getObligatoryCommonSet(self):
        return self.__obligatoryCommonSet

    def getOptionalCommonSet(self):
        counter = 0
        for course in self.__optionalCommonSet:
            if course.getIsDone():
                counter += int(course.getNumberOfHours())
        if counter < 6:
           return self.__optionalCommonSet
        else:
            return {}


    def getObligatoryCollageSet(self):
        return self.__obligatoryCollageSet

    def getObligatoryDegreeSet(self):
        return self.__obligatoryDegreeSet

    def getOptionalDegreeSet(self):
        counter = 0
        for course in self.__optionalDegreeSet:
            if course.getIsDone():
                counter += course.getNumberOfHours()

        if counter < 12:
            return self.__optionalDegreeSet
        else:
            return {}

    def getNumberOfCompletedHours(self):
        return self.__numberOfCompletedHours