from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def main():
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://central.carleton.ca/prod/bwysched.p_display_course?wsea_code=EXT&term_code=202230&disp=18299494&crn=34056")
    driver.maximize_window()

    term = driver.find_element(By.XPATH, "//td[contains(., 'Registration Term:')]//following-sibling::td")
    courseCode = driver.find_element(By.XPATH, "//td[contains(., 'Subject:')]//following-sibling::td")
    CRN = driver.find_element(By.XPATH, "//td[contains(., 'CRN:')]//following-sibling::td")
    title = driver.find_element(By.XPATH, "//td[contains(., 'Title:')]//following-sibling::td")
    description = driver.find_element(By.XPATH, "//td[contains(., 'Course Description:')]//following-sibling::td")
    credit = driver.find_element(By.XPATH, "//td[contains(., 'Course Credit Value:')]//following-sibling::td")

    print(term.text)
    print(courseCode.text)
    print(CRN.text)
    print(title.text)
    print(description.text)
    print(credit.text)


if __name__ == "__main__":
    main()