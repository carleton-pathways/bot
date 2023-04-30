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

    info_dict["term"] = driver.find_element(By.XPATH, "//td[contains(., 'Registration Term:')]//following-sibling::td").text
    info_dict["courseCode"] = driver.find_element(By.XPATH, "//td[contains(., 'Subject:')]//following-sibling::td").text
    info_dict["crn"] = driver.find_element(By.XPATH, "//td[contains(., 'CRN:')]//following-sibling::td").text
    info_dict["title"] = driver.find_element(By.XPATH, "//td[contains(., 'Title:')]//following-sibling::td").text
    info_dict["description"] = driver.find_element(By.XPATH, "//td[contains(., 'Course Description:')]//following-sibling::td").text
    info_dict["credit"] = driver.find_element(By.XPATH, "//td[contains(., 'Course Credit Value:')]//following-sibling::td").text
    info_dict["schedule_type"] = driver.find_element(By.XPATH, "//td[contains(., 'Schedule Type:')]//following-sibling::td").text
    info_dict["status"] = driver.find_element(By.XPATH, "//td[contains(., 'Status:')]//following-sibling::td").text
    info_dict["section_information"] = driver.find_element(By.XPATH, "//td[contains(., 'Section Information:')]//following-sibling::td").text
    info_dict["year_in_program"] = driver.find_element(By.XPATH, "//td[contains(., 'Year in Program:')]//following-sibling::td").text
    info_dict["level_restriction"] = driver.find_element(By.XPATH, "//td[contains(., 'Level Restriction:')]//following-sibling::td").text
    info_dict["degree_restriction"] = driver.find_element(By.XPATH, "//td[contains(., 'Degree Restriction:')]//following-sibling::td").text
    info_dict["major_restriction"] = driver.find_element(By.XPATH, "//td[contains(., 'Major Restriction:')]//following-sibling::td").text
    info_dict["program_restriction"] = driver.find_element(By.XPATH, "//td[contains(., 'Program Restrictions:')]//following-sibling::td").text
    info_dict["department_restriction"] = driver.find_element(By.XPATH, "//td[contains(., 'Department Restriction:')]//following-sibling::td").text
    info_dict["faculty_resitriction"] = driver.find_element(By.XPATH, "//td[contains(., 'Faculty Restriction:')]//following-sibling::td").text

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