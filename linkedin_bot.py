"""

	Desc: Bot to crawl onto linkedin and send out invitations to
		  users based on search criteria. To be used for educational
		  purposes when developing crawlers dealing with hidden elements.
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# sound
import subprocess

import numpy as np

from bs4 import BeautifulSoup

import random

from credentials import user, password, message, keyword, sound


#GLOBAL VALUES USED IN SCRIPT
url = "https://www.linkedin.com/uas/login?goback=&trk=hb_signin"
url_2 = 'https://www.linkedin.com/search/results/people/?facetNetwork=%5B%22S%22%5D&keywords=microsoft&origin=FACETED_SEARCH'
base_search_URL = 'https://www.linkedin.com/search/results/people/?keywords='


# SCRAPPER CLASS AND IT'S METHODS
class LinkedInScrapper():

	def __init__(self,username=user,password=password,message=message,search=keyword, sound_on = sound):
		self.driver = webdriver.Chrome(ChromeDriverManager().install())
		self.username = user
		self.password = password
		self.message = message
		self.search = keyword
		self.sound_on = sound
		self.driver.wait = WebDriverWait(self.driver,5)

	def Login(self):
		#lets get to the site
		self.driver.get(url)
		time.sleep(2)
		try:
			self.driver.find_element_by_name("session_key").send_keys(self.username)
			self.driver.find_element_by_name("session_password").send_keys(self.password+Keys.RETURN)
			time.sleep(2)	#give some time for the login.
		except Exception as a:
			print(str(a))

	def Search(self):
		#Lets search based on what keywords we chose
		#lets first compose the URL
		search_url = base_search_URL
		keywords = self.search.split(' ')
		# last = keywords.pop(len(keywords)-1)	#last word
		for word in keywords:
			search_url += word + '%20'
		search_url += "&origin=GLOBAL_SEARCH_HEADER"	#add the last word and the end parameters
		self.driver.get(search_url)
		if self.sound_on:
			subprocess.call(['afplay',"chinese-gong.wav"])


	def send_notesT(self):
		#This function queries all the buttons on the page
		#adding notes/invitations to only users who have not connected with you

		# class for connect button:


		# do 2, then scroll down a bit

		for i in range(0, 5):
			# scroll en bas puis choppe tous les noms

			time.sleep(3)
			scroll_delta = int(i)*150
			self.driver.execute_script("window.scrollBy(0, "+str(scroll_delta) + ")")

			all_names = self.driver.find_elements_by_class_name("actor-name")
			all_names_text = [x.text for x in all_names]

			if i == 0:
				unchecked = [x.text for x in all_names][:5]


			f = open('results.txt','a')
			f.write(str([x.text for x in all_names]) + 'unchecked: ' + str(unchecked) + 'all_names_text: ' + str(all_names_text) + '\n')

			time.sleep(2)

			if all_names[i].text == 'LinkedIn Member':
				continue
			else:
				all_names[np.where(all_names_text == unchecked[0])[0][0]].click()
				unchecked = unchecked[1:]
				# all_names[i].click()
				time.sleep(2)

				# include if has pending instead of connect
				# try:
				# 	self.driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']").click()
				# except NoSuchElementException:
				# 	self.driver.find_element_by_xpath("//*[@class='ml2 pv-s-profile-actions__overflow-toggle artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary ember-view']/span").click()
				# 	try:
				# 		# If invitation has already been sent, then go to next employee.
				# 		if self.driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect pv-s-profile-actions__overflow-button full-width text-align-left  ember-view']/span[1]").text == "Pending":
				# 			self.driver.execute_script("window.history.go(-1)")
				# 			continue
				# 	except NoSuchElementException:
				# 		try:
				# 			self.driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect pv-s-profile-actions__overflow-button full-width text-align-left ember-view']/span[1]").click()
				# 		except NoSuchElementException:
				# 			continue

				# time.sleep(1)
				# self.driver.find_element_by_xpath("//button[@aria-label='Add a note']").click()
				# time.sleep(1)
				# self.driver.find_element_by_name("message").send_keys(self.message)
				# time.sleep(1)
				# self.driver.find_element_by_xpath("//button[@aria-label='Send invitation']").click()
				self.driver.execute_script("window.history.go(-1)")
		f.write('second for loop'+'\n')

		unchecked = []


		for i in range(5,10):
			time.sleep(3)
			# scroll_delta = 5*150 + (int(i)-5)*130

			scroll_delta = 5*170 + (int(i)-5)*110
			self.driver.execute_script("window.scrollBy(0, "+str(scroll_delta) + ")")

			time.sleep(1)

			all_names = self.driver.find_elements_by_class_name("actor-name")
			all_names_text = [x.text for x in all_names]

			if len(all_names) == 10:
				unchecked = [x.text for x in all_names][5:]


			f = open('results.txt','a')
			f.write('iter loop:' + str(i) + ' ' + str(len(all_names)) + ' ' + str([x.text for x in all_names]) + str(all_names[i].text) + '\n')

			time.sleep(2)

			being_checked = all_names[i]
			being_checked_text = being_checked.text

			if being_checked.text == 'LinkedIn Member':
				continue
			else:
				if len(all_names)==10:
					being_checked.click()
					time.sleep(1)
					unchecked = unchecked[unchecked != being_checked_text]
				else:
					# click on element with text = unchecked[0]
					all_names[np.where(all_names_text == unchecked[0])[0][0]].click()
					unchecked = unchecked[1:]

			time.sleep(2)

			self.driver.execute_script("window.history.go(-1)")





				# elif all_names[i].text == unchecked[0]:
				# 	all_names[i].click()
				# 	unchecked = unchecked[unchecked != all_names[i].text]









	def send_notes(self):
		#This function queries all the buttons on the page
		#adding notes/invitations to only users who have not connected with you

		#Lets wait for the buttons to load
		time.sleep(4)
		WebDriverWait(self.driver,120).until(EC.presence_of_element_located((By.CSS_SELECTOR,".search-result__actions--primary.button-secondary-medium.m5")))
		#Lets grab all the buttons
		Buttons = self.driver.execute_script("return document.querySelectorAll('.search-result__actions--primary.button-secondary-medium.m5').length")
		for i in range(0,Buttons):
			#Check if button still says connect
			if("Connect" in self.driver.execute_script("return document.querySelectorAll('.search-result__actions--primary.button-secondary-medium.m5')["+str(i)+"].textContent")):
				self.driver.execute_script("document.querySelectorAll('.search-result__actions--primary.button-secondary-medium.m5')["+str(i)+"].click()")
				#Find the dialoug box that the Javascript brought up
				self.driver.execute_script("document.querySelectorAll('button.button-secondary-large')[1].click()")
				self.driver.find_element_by_name("message").send_keys(self.message)
				#send invitation
				self.driver.find_element_by_css_selector(".button-primary-large.ml3").click()
			#Done, lets wait for page to load a bit
			time.sleep(2)


	def nextPage(self):
		#Head to the next page
		if self.sound_on:
			subprocess.call(['afplay',"chinese-gong.wav"])
		else:
			time.sleep(2)	#lets wait for page to load
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

		time.sleep(1)
		self.driver.find_element_by_xpath("//button[@aria-label='Next']").click()


if __name__ == "__main__":
	#Call the function
	L = LinkedInScrapper()
	L.Login()
	L.Search()
	while True:
		L.send_notesT()
		L.nextPage()
