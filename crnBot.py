from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
import pandas as pd

START_CRN = 30000
END_CRN = 30010


def main():

    df = pd.DataFrame(columns=['termCode', 'CRN',])
    df_counter = 0

    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = options)

    terms = [
        {
        "name": "Fall2022",
        "urlValue": 202230,
        "validCRNs": [],
        },
        {
        "name": "Winter2023",
        "urlValue": 202310,
        "validCRNs": [],
        },
        {
        "name": "Summer2023",
        "urlValue": 202320,
        "validCRNs": [],
        },
    ]

    urlFirst = "https://central.carleton.ca/prod/bwysched.p_display_course?wsea_code=EXT&term_code="
    urlSecond = "&disp=18292988&crn="

    for term in terms:
        # print(term)
        url = urlFirst + str(term["urlValue"]) + urlSecond

        for j in range(START_CRN, END_CRN):
            driver.get(url + str(j))

            if driver.find_elements(By.CLASS_NAME, 'warningtext'):
                continue
            else:
                term["validCRNs"].append(j)
                df.loc[df_counter] = [term["urlValue"], j]
                df_counter += 1

        # print(term["validCRNs"])
        # print(df)

if __name__ == "__main__":
    main()