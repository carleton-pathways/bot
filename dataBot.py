from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import dataParser

def main():

    parser = dataParser.DataParser()

    term_array = ['Registration Term', 'Subject', 'CRN', 'Title', 'Course Description', 'Course Credit Value', 'Schedule Type', 'Status', 'Section Information', 'Year in Program',
                  'Level Restriction', 'Degree Restriction', 'Major Restriction', 'Program Restrictions', 'Department Restriction', 'Faculty Restriction', 'Meeting Date', 'Days', 
                  'Time', 'Building', 'Room', 'Schedule', 'Instructor',]
    
    cols = ['registration_term', 'faculty', 'course_code', 'section', 'tut_id', 'crn', 'title', 'course_description', 'precludes_string', 'precludes_courses', 'prereq_string', 'prereq_courses',
            'course_credit_value', 'schedule_type', 'status', 'section_information', 'year_in_program', 'level_restriction', 'degree_restriction', 'major_restriction', 'program_restrictions', 
            'department_restriction', 'faculty_restriction', 'start_date', 'end_date', 'days', 'start_time', 'end_time', 'building', 'room', 'schedule', 'instructor', 'instructor_status']

    df = pd.DataFrame(columns=cols)

    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://central.carleton.ca/prod/bwysched.p_display_course?wsea_code=EXT&term_code=202320&disp=18299494&crn=20169")
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    secondtable = soup.findAll('table')[1]

    info = []
    
    # finds everything in first table
    for i in range(0, 16):
        result = []
        text = driver.find_element(By.XPATH, "//td[contains(., '%s:')]//following-sibling::td"%(term_array[i])).text
        term = (term_array[i].replace(" ", "_")).lower()

        if (term == "course_description"):
            result.append(text)
            result.extend(parser.parse(term, text, additional_credit=True))
            result.extend(parser.parse(term, text, additional_credit=False))
        else:
            result.extend(parser.parse(term, text))
        info.extend(result)
    
    # finds everything in second table
    for i, col in enumerate(secondtable.find_all("tr")[1].find_all("td")):
        result = []
        term = (term_array[i+16].replace(" ", "_")).lower()
        result.extend(parser.parse(term, col.text))

        info.extend(result)

    df.loc[len(df)] = info

    df.to_csv("course_data.csv", index=False)


if __name__ == "__main__":
    main()