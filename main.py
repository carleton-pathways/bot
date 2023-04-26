from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = options)

driver.get("https://central.carleton.ca/prod/bwysched.p_select_term?wsea_code=EXT")
driver.maximize_window()

# initialize and select the dropdown menu
dropdownbox = driver.find_element(By.NAME, "term_code")
select = Select(dropdownbox)
select.select_by_visible_text("Winter 2023 (January-April)")

#click the button
search = driver.find_element(By.XPATH, "//input[@title='Click to search for courses offered in the term selected above']")
search.click()

#determining course level
crlevl = Select(driver.find_element(By.ID, "levl_id"))
crlevl.select_by_visible_text("All Levels")

#determining subject
sbjlevl = Select(driver.find_element(By.ID, "subj_id"))
sbjlevl_el = driver.find_element(By.ID, "subj_id")

# Open the sbjlevl dropdown menu and scroll down
sbjlevl_el.click()
for _ in range(10):
    sbjlevl_el.send_keys(Keys.ARROW_DOWN)

# Get all the options in the sbjlevl dropdown menu
options = sbjlevl.options

sbjlevl.select_by_index(1)
# for option in options:
#     print(option.text)

#seachnext
search = driver.find_element(By.XPATH, "//input[@title='Search for courses based on my criteria']")
search.click()


first = driver.find_element(By.CSS_SELECTOR, "/html/body/section/section/form/table/tbody/tr[4]/td/div/table/tbody/tr[1]/td[6]")
first.click()