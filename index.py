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
                  'Level Restriction', 'Degree Restriction', 'Major Restriction', 'Program Restrictions', 'Department Restriction', 'Faculty Restriction',]
    
    # finds everything in first table
    for term in term_array:
        info_dict[(term.replace(" ", "_")).lower()] = driver.find_element(By.XPATH, "//td[contains(., '%s:')]//following-sibling::td"%(term)).text

    # finds everything in second table
    for i, col in enumerate(secondtable.find_all("tr")[1].find_all("td")):
        if (i == 0):
            info_dict["meeting_date"] = col.text
        elif (i == 1):
            info_dict["days"] = col.text
        elif (i == 2):
            info_dict["time"] = col.text
        elif (i == 3):
            info_dict["building"] = col.text
        elif (i == 4):
            info_dict["room"] = col.text
        elif (i == 5):
            info_dict["schedule"] = col.text
        elif (i == 6):
            info_dict["instructor"] = col.text


    print(info_dict)

if __name__ == "__main__":
    main()