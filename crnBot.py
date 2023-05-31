from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
import pandas as pd

URL_FIRST = "https://central.carleton.ca/prod/bwysched.p_display_course?wsea_code=EXT&term_code="
URL_SECOND = "&disp=18292988&crn="

CRN_CSV_PATH = 'crns.csv'

class CrnBot:

    def __init__(self):
        self.df = pd.DataFrame(columns=['termCode', 'crns',])
        self.terms = [
            {
            "name": "W2023",
            "urlValue": "202310",
            "validCRNs": [],
            "startCRN": 10000,
            "endCRN" : 10009,
            },
            {
            "name": "S2023",
            "urlValue": "202320",
            "validCRNs": [],
            "startCRN": 20000,
            "endCRN" : 20009,
            },
        ]

        options = Options()
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options = options)

    def scrape(self):
        for term in self.terms:
            url = URL_FIRST + (term["urlValue"]) + URL_SECOND
            for j in range(term["startCRN"], term["endCRN"]):
                self.driver.get(url + str(j))

                if not self.driver.find_elements(By.CLASS_NAME, 'warningtext'):
                    term["validCRNs"].append(j)
                    
            self.df.loc[len(self.df)] = [term["urlValue"], term["validCRNs"]]

        self.driver.close()

        self.df.to_csv(CRN_CSV_PATH, index=False)