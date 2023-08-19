import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from src.handler.parse.automating import *



class Webhelper:
    
    thing = "Thing"
    
    def __init__(self):
        self.description = "A webhelper"
        self.information = {}
        self.parameters = {}
        self.objects = {}
        self.functions = {}
    
    def get_geckodriver():
        from selenium.webdriver import Firefox
        from selenium.webdriver.firefox.options import Options

        options = Options()
        options.headless = True

        driver = webdriver.Firefox(
            #options=options,
            executable_path=r'C:/Users/Bill/projects/firefox/geckodriver.exe'
        )
        return driver
    
    def initialize(self):
        print("par:", self.description)    

class Webhelper(object):

    def __init__(self):
        self.driver = get_geckodriver()  # webdriver.Chrome(executable_path="chromedriver.exe")
        self.initialize()
    
    def initialize(self):
        self.get("https://bard.google.com/")
        time.sleep(5)
        self.sign_in()

    def get(self, url):
        self.driver.get(url)
        prev = ""
        for _ in range(5):
            page_source = self.driver.page_source
            # maybe by length, dynamic can stop this
            if prev != page_source:
                prev = page_source
            else:
                print("prev, curr lengths", len(prev), len(page_source))
                pass

    def get_waited_element_by_xpath(self, xpath, limit=6):
        """
        gets an element waiting at most limit seconds
        """
        start_time = datetime.datetime.now()
        element = None
        curr_time = datetime.datetime.now()
        while not element and int((curr_time - start_time).total_seconds()) < limit:
            element = self.driver.find_element(By.XPATH, xpath)
            if element:
                return element
            time.sleep(1)
            curr_time = datetime.datetime.now()
        return None
    
    def select(self, XPATH, index):
        # could convert to waited
        select_element = self.driver.find_element(By.XPATH, XPATH)
        if not select_element:
            return False
        select_element = Select(select_element)
        select_element.select_by_index(index)
        return True

    def write(self, XPATH, keys):
        # could convert to waited
        input_box = self.get_waited_element_by_xpath(XPATH)
        if not input_box:
            return False
        input_box.send_keys(keys)
        return True

    def click(self, XPATH):
        """
        Returns whether the click attempt was successful
        """
        # could convert to waited

        object = self.driver.find_element(By.XPATH, XPATH)
        # check whether the object is clickable (2 conditions must be satisfied)
        if object.is_displayed() and object.is_enabled():
            # this can still cause a crash, as some elements are obscured or hidden
            # i.e. a label is clickable, but can be obscured by a sometimes clickable
            # label associated with the label.
            object.click()
        else:
            print("Element is not clickable")

        time.sleep(1)
        return True