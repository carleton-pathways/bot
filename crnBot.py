from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
import pandas as pd

URL_FIRST = "https://central.carleton.ca/prod/bwysched.p_display_course?wsea_code=EXT&term_code="
URL_SECOND = "&disp=18292988&crn="

df = pd.DataFrame(columns=['termCode', 'crns',])

def main():
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = options)

    terms = [
        {
        "name": "F2022",
        "urlValue": 202230,
        "validCRNs": [],
        "startCRN": 30000,
        "endCRN" : 30009,
        },
        {
        "name": "W2023",
        "urlValue": 202310,
        "validCRNs": [],
        "startCRN": 10000,
        "endCRN" : 10009,
        },
        {
        "name": "S2023",
        "urlValue": 202320,
        "validCRNs": [],
        "startCRN": 20000,
        "endCRN" : 20009,
        },
    ]

    for term in terms:
        url = URL_FIRST + str(term["urlValue"]) + URL_SECOND

        for j in range(term["startCRN"], term["endCRN"]):
            
            driver.get(url + str(j))

            if not driver.find_elements(By.CLASS_NAME, 'warningtext'):
                term["validCRNs"].append(j)
                
        df.loc[len(df)] = [term["urlValue"], term["validCRNs"]]

    df.to_csv("crns.csv", index=False)

if __name__ == "__main__":
    main()