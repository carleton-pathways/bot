from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By


def main():
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = options)
    driver.get("https://central.carleton.ca/prod/bwysched.p_display_course?wsea_code=EXT&term_code=202230&disp=18299494&crn=34056")
    driver.maximize_window()

    b_element = driver.find_element(By.XPATH, "//b[contains(text(), 'target text')]")

    # 2. Go backwards to the <tr> element
    tr_element = b_element.find_element(By.XPATH, "./sibling::tr")

    # 3. Print the other <td> elements inside the <tr>
    td_elements = tr_element.find_elements(By.XPATH,"./td")
    for td in td_elements:
        if td != b_element:
            print(td.text)

if __name__ == "__main__":
    main()
