from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from ast import literal_eval
import dataParser

URL_FIRST = "https://central.carleton.ca/prod/bwysched.p_display_course?wsea_code=EXT&term_code="
URL_SECOND = "&disp=18292988&crn="

CRN_CSV_PATH = 'crns.csv'
COURSE_DATA_CSV_PATH = "course_data.csv"

COURSE_INFO_LENGTH = 33

class DataBot:
    TERM_ARRAY = ['Registration Term', 'Subject', 'CRN', 'Title', 'Course Description', 'Course Credit Value', 'Schedule Type', 'Status', 'Section Information', 'Year in Program',
                    'Level Restriction', 'Degree Restriction', 'Major Restriction', 'Program Restrictions', 'Department Restriction', 'Faculty Restriction', 'Meeting Date', 'Days', 
                    'Time', 'Building', 'Room', 'Schedule', 'Instructor',]
        
    cols = ['registration_term', 'faculty', 'course_code', 'section', 'tut_id', 'crn', 'title', 'course_description', 'precludes_string', 'precludes_courses', 'prereq_string', 'prereq_courses',
        'course_credit_value', 'schedule_type', 'status', 'section_information', 'year_in_program', 'level_restriction', 'degree_restriction', 'major_restriction', 'program_restrictions', 
        'department_restriction', 'faculty_restriction', 'start_date', 'end_date', 'days', 'start_time', 'end_time', 'building', 'room', 'schedule', 'instructor', 'instructor_status']

    df = pd.DataFrame(columns=cols)
    parser = dataParser.DataParser()

    def __init__(self):
        
        options = Options()
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scrape(self):
        
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        secondtable = soup.findAll('table')[1]

        info = []
        
        # finds everything in first table
        for i in range(0, 16):
            text = self.driver.find_element(By.XPATH, "//td[contains(., '%s:')]//following-sibling::td"%(self.TERM_ARRAY[i])).text
            term = (self.TERM_ARRAY[i].replace(" ", "_")).lower()
            info.extend(self.parser.parse(term, text))

        # finds everything in second table
        secondTableEnumerable = (secondtable.find_all("tr"))

        if (len(secondTableEnumerable) == 0):
            info.extend([None for n in range(COURSE_INFO_LENGTH - len(info))])
        else:
            secondTableEnumerable = secondTableEnumerable[1].find_all("td")
            for j in range(7):
                if (j >= len(secondTableEnumerable)):
                    info.extend([None for n in range(COURSE_INFO_LENGTH - len(info))])
                    break

                term = (self.TERM_ARRAY[j+16].replace(" ", "_")).lower()
                info.extend(self.parser.parse(term, secondTableEnumerable[j].text))

        return info

    def run(self):
        crns = pd.read_csv(CRN_CSV_PATH)
        crns.crns = crns.crns.apply(literal_eval)

        for index, row in crns.iterrows():
            for crn in row['crns']:
                self.driver.get(URL_FIRST + str(row['termCode']) + URL_SECOND + str(crn))
                self.df.loc[len( self.df)] = self.scrape()
                
        self.df.to_csv(COURSE_DATA_CSV_PATH, index=False)
