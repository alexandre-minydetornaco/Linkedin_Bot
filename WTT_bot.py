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
import re

# GLOBAL VALUES USED IN SCRIPT
#url = "https://www.welcometothejungle.com/fr/jobs#signin?ref=header"
url = "https://www.welcometothejungle.com/fr/jobs?page=1&configure%5Bfilters%5D=website.reference%3Awttj_fr&configure%5BhitsPerPage%5D=30&aroundQuery=France&refinementList%5Boffice.country_code%5D%5B%5D=FR&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Stage&query=%22data%20analyst%22&range%5Bexperience_level_minimum%5D%5Bmin%5D=0&range%5Bexperience_level_minimum%5D%5Bmax%5D=1"
url_2 = 'https://www.welcometothejungle.com/fr/companies/kapten/jobs/data-analyst-h-f-cdi-paris_levallois-perret_KAPTE_8m2plWg'
base_search_URL = 'https://www.welcometothejungle.com/fr/jobs?query=%22Data%20Analyst%22'


# SCRAPPER CLASS AND IT'S METHODS
class WTTScrapper():

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.wait = WebDriverWait(self.driver, 1)

    def Login(self):
         # lets get to the site
         self.driver.get(url)

    def click(self):
#        for i in range(1, 31, 1):
#            i = 1
#       offer = self.driver.find_elements_by_xpath(f'//*[@id="app"]/div/div/main/section/div/div[1]/ul/li[{i}]')
        self.driver.find_element_by_class_name("ais-Hits-item").click()

    def getText(self):

        data = self.driver.page_source
        soup = BeautifulSoup(data, 'html.parser')
        result = soup.find(string=re.compile("Profil recherché"))
        print(str(result))

        #text = result.next_sibling.get_text()
        #f = open('results.txt', 'a')
        #f.write(text.encode('utf-8').decode('ascii', 'ignore'))

    def getText2(self):

        text = self.driver.find_element_by_xpath("//*[@class='sc-12bzhsi-16 eXgLWp'][text()[contains(.,'Profil recherché')]]").text
        f = open('results.txt', 'a')
        f.write(str(text))



L = WTTScrapper()
L.Login()
L.click()
L.getText2()

#	def Search(self):
#		#Lets search based on what keywords we chose
#		#lets first compose the URL
#		search_url = base_search_URL
#		keywords = self.search.split(' ')
#		# last = keywords.pop(len(keywords)-1)	#last word
#		for word in keywords:
#			search_url += word + '%20'
#		search_url += "&origin=GLOBAL_SEARCH_HEADER"	#add the last word and the end parameters
#		self.driver.get(search_url)
#		if self.sound_on:
#			subprocess.call(['afplay',"chinese-gong.wav"])

# 	def send_notes(self):
# 		#This function queries all the buttons on the page
# 		#adding notes/invitations to only users who have not connected with you
#
# 		# class for connect button:
#
# 		# do 2, then scroll down a bit
#
# 		for i in range(0, 5):
# 			# scroll en bas puis choppe tous les noms
# 			time.sleep(3)
# 			scroll_delta = int(i)*140
# 			self.driver.execute_script("window.scrollBy(0, "+str(scroll_delta) + ")")
#
# 			all_names = self.driver.find_elements_by_class_name("actor-name")
# 			all_names_text = [x.text for x in all_names]
#
# 			if i == 0:
# 				unchecked = [x.text for x in all_names][:5]
#
# 			f = open('results.txt','a')
# 			f.write(str([x.text for x in all_names]) + 'unchecked: ' + str(unchecked) + '\n')
#
# 			time.sleep(2)
#
# 			if all_names[i].text == 'LinkedIn Member':
# 				continue
# 			else:
# 				all_names[np.where(np.array(all_names_text) == unchecked[0])[0][0]].click()
# 				unchecked = unchecked[1:]
# 				time.sleep(3)
#
# 				# # include if has pending instead of connect
# 				# try:
# 				# 	driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']").click()
# 				# except NoSuchElementException:
# 				# 	driver.find_element_by_xpath("//*[@class='ml2 pv-s-profile-actions__overflow-toggle artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary ember-view']/span").click()
# 				#
# 				# 	try:
# 				# 		# If invitation has already been sent, then go to next employee.
# 				# 		if driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect pv-s-profile-actions__overflow-button full-width text-align-left  ember-view']/span[1]").text == "Pending":
# 				# 			driver.execute_script("window.history.go(-1)")
# 				# 			continue
# 				#
# 				# 	except NoSuchElementException:
# 				# 		try:
# 				# 			driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect pv-s-profile-actions__overflow-button full-width text-align-left ember-view']/span[1]").click()
# 				# 		except NoSuchElementException:
# 				# 			continue
# 				# time.sleep(1)
# 				# driver.find_element_by_xpath("//button[@aria-label='Add a note']").click()
# 				# time.sleep(1)
# 				# driver.find_element_by_name("message").send_keys(self.message)
# 				# time.sleep(1)
# 				# driver.find_element_by_xpath("//button[@aria-label='Send invitation']").click()
#
# 				self.driver.execute_script("window.history.go(-1)")
#
# 		f.write('second for loop'+'\n')
#
# 		unchecked = []
#
#
# 		for i in range(5,10):
# 			time.sleep(3)
# 			# scroll_delta = 5*150 + (int(i)-5)*130
#
# 			scroll_delta = 5 * 170 + (int(i)-5) * 110
# 			self.driver.execute_script("window.scrollBy(0, "+str(scroll_delta) + ")")
#
# 			time.sleep(1)
#
# 			all_names = self.driver.find_elements_by_class_name("actor-name")
# 			all_names_text = [x.text for x in all_names]
#
# 			if i == 5:
# 				unchecked = [x.text for x in all_names][5:]
#
# 			f = open('results.txt','a')
# 			f.write('iter loop:' + str(i) + ' ' + str(len(all_names)) + ' ' + str([x.text for x in all_names]) + ' ' + str(unchecked) + '\n')
#
# 			time.sleep(2)
#
# 			if unchecked[0] == 'LinkedIn Member':
# 				continue
# 			else:
# 				# click on element with text = unchecked[0]
# 				all_names[np.where(np.array(all_names_text) == unchecked[0])[0][0]].click()
# 				unchecked = unchecked[1:]
#
# 			time.sleep(2)
#
# 			self.driver.execute_script("window.history.go(-1)")
#
#
# 	def nextPage(self):
# 		#Head to the next page
# 		if self.sound_on:
# 			subprocess.call(['afplay',"chinese-gong.wav"])
# 		else:
# 			time.sleep(2)	#lets wait for page to load
# 		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#
# 		time.sleep(1)
# 		self.driver.find_element_by_xpath("//button[@aria-label='Next']").click()
#
#
# if __name__ == "__main__":
# 	#Call the function
# 	L = LinkedInScrapper()
# 	L.Login()
# 	L.Search()
# 	while True:
# 		L.send_notes()
# 		L.nextPage()
