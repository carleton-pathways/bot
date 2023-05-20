from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd


def main():
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://central.carleton.ca/prod/bwysched.p_display_course?wsea_code=EXT&term_code=202230&disp=18299494&crn=30001")
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    secondtable = soup.findAll('table')[1]
    
    info_dict = {}

    term_array = ['Registration Term', 'Subject', 'CRN', 'Title', 'Course Description', 'Course Credit Value', 'Schedule Type', 'Status', 'Section Information', 'Year in Program',
                  'Level Restriction', 'Degree Restriction', 'Major Restriction', 'Program Restrictions', 'Department Restriction', 'Faculty Restriction', 'Meeting Date', 'Days', 
                  'Time', 'Building', 'Room', 'Schedule', 'Instructor',]
    
    # finds everything in first table
    for i in range(0, 15):
        info_dict[(term_array[i].replace(" ", "_")).lower()] = driver.find_element(By.XPATH, "//td[contains(., '%s:')]//following-sibling::td"%(term_array[i])).text

    # finds everything in second table
    for i, col in enumerate(secondtable.find_all("tr")[1].find_all("td")):
        info_dict[(term_array[i+16].replace(" ", "_")).lower()] = col.text

    # print(info_dict)

if __name__ == "__main__":
    main()