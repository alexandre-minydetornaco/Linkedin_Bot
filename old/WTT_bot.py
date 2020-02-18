"""

	Desc: Bot to crawl onto linkedin and send out invitations to
		  users based on search criteria. To be used for educational
		  purposes when developing crawlers dealing with hidden elements.
"""
# sound
import subprocess
import time

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests

import re

# GLOBAL VALUES USED IN SCRIPT
#url = "https://www.welcometothejungle.com/fr/jobs#signin?ref=header"
url = "https://www.welcometothejungle.com/fr/jobs?page=1&configure%5Bfilters%5D=website.reference%3Awttj_fr&configure%5BhitsPerPage%5D=30&aroundQuery=France&refinementList%5Boffice.country_code%5D%5B%5D=FR&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Stage&query=%22data%20analyst%22&range%5Bexperience_level_minimum%5D%5Bmin%5D=0&range%5Bexperience_level_minimum%5D%5Bmax%5D=1"
url_2 = 'https://www.welcometothejungle.com/fr/companies/kapten/jobs/data-analyst-h-f-cdi-paris_levallois-perret_KAPTE_8m2plWg'
base_search_URL = 'https://www.welcometothejungle.com/fr/jobs?query=%22Data%20Analyst%22'


# SCRAPPER CLASS AND IT'S METHODS
class WTTScrapper():

    def __init__(self):
        '''Init bot'''
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.wait = WebDriverWait(self.driver, 1)


    def MainPage(self):
        '''Go the the first page'''
        self.driver.get(url)

    def Click(self, pos):
        '''Click on the link'''
        self.driver.find_elements_by_class_name("ais-Hits-item")[pos].click()

    def GetText(self):
        #data = self.driver.page_source
        data = requests.get(self.driver.current_url)
        #data = requests.get("https://www.welcometothejungle.com/fr/companies/jellysmack/jobs/data-analyst-h-f-corse_corte")
        soup = BeautifulSoup(data.text, 'html.parser',from_encoding="utf-8")
        h1 = soup.find("div", {"class": "sc-11obzva-1 czRmi"})
        h2 = h1.findAll("div", {"class": "sc-11obzva-1 czRmi"})
        h3 = h2[2]
        f = open('results.txt', 'a')
        f.write(h3.get_text())
        f.write('\n')
        f.close()

L = WTTScrapper()
L.MainPage()
L.Click(1)
L.GetText()