import random
import time
import re
import json
import openai
import requests
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
            self.write("//input[@id='username']", "bilan604@yahoo.com")
            self.write("//input[@id='password']", "6047822691aA")
            self.click("//button[@class='btn__primary--large from__button--floating']")
    


def load_company_insights(id, profile_url):
    searcher = Searcher("bilan604@yahoo.com", "6047822691aA##", "LinkedIn")
    searcher.get_insights(profile_url)

    return "Placeholder"