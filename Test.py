from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep
import re
from enum import Enum
import pyodbc


class Major(Enum):
    CS = 1
    SE = 2
    CIS = 3
    CG = 4


class Student:
    def __init__(self, username, password, major):
        self.__courses = self.__getCourses(username, password)
        self.__major = Major(major).name

    def __getCourses(self, username, password):
        courses = set()
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

            c = 0
            for i in range(4, 20, 2):
                try:
                    table = driver.find_elements(By.TAG_NAME, 'table')[i]
                    for row in table.find_elements(By.TAG_NAME, 'tr'):
                        cells = row.find_elements(By.TAG_NAME, 'td')
                        cell_texts = [cell.text for cell in cells]
                        print(cell_texts[0], " ", cell_texts[1])
                        c += 1
                        if cell_texts[0] != 'رقم المادة' and (
                                re.match(r'([ABCF][+-]?|D[+]?)', cell_texts[3]) or cell_texts[3] == 'ناجح'):
                            courses.add(cell_texts[0])
                except IndexError:
                    continue
            print(c)
        finally:
            driver.quit()

        return courses

    def getCourses(self):
        return self.__courses

    def getDegree(self):
        return self.__major


# student = Student("", "",1)


file_path = r'C:\Users\hp\Desktop\Python Project\CS.txt'
database_path = r'C:\Users\hp\Documents\CoursesProject.accdb'

# Establishing connection
conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + database_path + ';'
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Splitting each line assuming it's space-separated
            parts = line.split()
            if len(parts) >= 2:
                ID = parts[0]
                name = ' '.join(parts[1:])  # Joining the rest as name
                if name.__contains__('مختبر'):
                    Hours = 1
                elif name.__contains__('التدربب'):
                    Hours = 6
                else:
                    Hours = 3

                # Inserting into database
                insert_sql = '''
                INSERT INTO ComputerScience (Name, ID,Hours,Optional)
                VALUES (?, ? , ?,Yes)
                '''
                cursor.execute(insert_sql, (name, ID, Hours))

    # Committing changes
    conn.commit()
    print("Data successfully inserted into the database.")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    # Closing connection
    conn.close()







# # Define the path to your Access database
# database_path = r'C:\Users\hp\Documents\CoursesProject.accdb'
#
# # Create a connection string
# conn_str = (
#     r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
#     r'DBQ=' + database_path + ';'
# )
#
# # Establish a connection to the database
# conn = pyodbc.connect(conn_str)
#
# # Create a cursor object to interact with the database
# cursor = conn.cursor()
#
# # Define the SQL statement to create the table
# create_table_sql = '''
# CREATE TABLE ComputerScience (
#     Name VARCHAR(50),
#     ID VARCHAR(20),
#     Year INT,
#     Rank INT,
#     Lab BIT,
#     Hours INT,
#     Optional BIT
# )
# '''
#
# # Execute the create table SQL statement
# cursor.execute(create_table_sql)
#
# # Commit the transaction
# conn.commit()
#
# # Close the connection
# conn.close()
# print("Table 'Courses' created successfully.")



