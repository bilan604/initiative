
import re
import time
import openai
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class Searcher(object):
    
    def __init__(self, username, password, platform):
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")
        self.username = username
        self.password = password
        self.platform = platform
        self.login(platform)
    
    def get_waited(self, xpath):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    
    def select(self, XPATH, index):
        select_element = Select(self.driver.find_element(By.XPATH, XPATH))
        select_element.select_by_index(index)
    
    def write(self, XPATH, keys):
        self.get_waited(XPATH).send_keys(keys)
    
    def click(self, XPATH):
        self.get_waited(XPATH).click()

    def upload_resume(self, file_path):
        # absolute filepath from c:
        self.get_waited("//input[@name ='personal.resume']").send_keys(file_path)

    def login(self, platform):
        if platform == "LinkedIn":
            self.driver.get("https://www.linkedin.com/login")
            self.write("//input[@id='username']", "")
            self.write("//input[@id='password']", "")
            self.click("//button[@class='btn__primary--large from__button--floating']")
    
    def get_insights(self, url):
        if url[-1] == "/":
            url = url[:-1]
        self.driver.get(url + "/people/")
        self.write("//input[@id='people-search-keywords']", "engineer")
        self.write("//input[@id='people-search-keywords']", Keys.ENTER)
        
        waiter = self.get_waited("//div[@class='insight-container__title']")

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        people = soup.find_all('h2', {"class": "t-20 t-black t-bold"})
        people = list(map(str, people))
        people = [re.sub("<.+?>", "", p).strip() for p in people]
        print(people, "people--")
        
        by_region = soup.find_all("div", {"class": "org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal"})
        by_region = list(map(str, by_region))
        by_region = [re.sub("<.+?>", " ", br).strip() for br in by_region]
        by_region = [br.split("\n")[0].strip() for br in by_region if "United States" in br]
        print(by_region,"by_region")
        time.sleep(20)


def load_company_insights(id, profile_url):
    searcher = Searcher("", "", "LinkedIn")
    searcher.get_insights(profile_url)

    return "Placeholder"