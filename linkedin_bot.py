"""
	Author: Xavid Ramirez
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
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from credentials import user, password, message, keyword


#GLOBAL VALUES USED IN SCRIPT
url = "https://www.linkedin.com/uas/login?goback=&trk=hb_signin"
url_2 = 'https://www.linkedin.com/search/results/people/?facetNetwork=%5B%22S%22%5D&keywords=microsoft&origin=FACETED_SEARCH'
base_search_URL = 'https://www.linkedin.com/search/results/people/?keywords='
#Webdriver Paths
# Chromedriver_Path = r'PATH TO CROME DRIVER'
# Chrome_Options = Options().add_argument('--test-type')
#END OF GLOBAL VALUES

# SCRAPPER CLASS AND IT'S METHODS
class LinkedInScrapper():

	def __init__(self,USERNAME,PASSWORD,MESSAGE,SEARCH):
		self.driver = webdriver.Chrome(ChromeDriverManager().install())
		self.username = USERNAME
		self.password = PASSWORD
		self.message = MESSAGE
		self.search = SEARCH
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

	def nextPage(self):
		#Head to the next page
		time.sleep(2)	#lets wait for page to load
		Button = self.driver.execute_script("return document.querySelectorAll('button.next')[0]")
		if(Button != None):
			self.driver.execute_script("document.querySelectorAll('button.next')[0].click()")


	def send_notes(self):
		#This function queries all the buttons on the page
		#adding notes/invitations to only users who have not connected with you

		# class for connect button:
		all_connect = self.driver.find_elements_by_xpath("//*[@class='search-entity search-result search-result--person search-result--occlusion-enabled ember-view']/div/div[1]")
		all_names = self.driver.find_elements_by_class_name("actor-name")

		# do 2, then scroll down a bit

		for i in range(0, len(all_connect)):
			time.sleep(3)
			all_connect = self.driver.find_elements_by_xpath("//*[@class='search-entity search-result search-result--person search-result--occlusion-enabled ember-view']/div/div[1]")
			all_names = self.driver.find_elements_by_class_name("actor-name")

			if all_names[i].text == 'LinkedIn Member':
				continue
			else:
				all_connect[i].click()
				time.sleep(2)

				# include if has pending instead of connect
				try:
					self.driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']").click()
				except NoSuchElementException:
					self.driver.find_element_by_xpath("//*[@class='ml2 pv-s-profile-actions__overflow-toggle artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary ember-view']/span").click()
					try:
						# If invitation has already been sent, then go to next employee.
						if self.driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect pv-s-profile-actions__overflow-button full-width text-align-left  ember-view']/span[1]").text == "Pending":
							self.driver.execute_script("window.history.go(-1)")
							continue
					except NoSuchElementException:
						self.driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect pv-s-profile-actions__overflow-button full-width text-align-left ember-view']/span[1]").click()

				time.sleep(1)
				self.driver.find_element_by_xpath("//button[@aria-label='Add a note']").click()
				time.sleep(1)
				self.driver.find_element_by_name("message").send_keys(self.message)
				time.sleep(1)
				self.driver.find_element_by_xpath("//button[@aria-label='Send invitation']").click()
				self.driver.execute_script("window.history.go(-1)")
				if i%2==0:
					self.driver.execute_script("window.scrollBy(0, -20)")





## HERE WE WILL START THE SCRAPPER
def main(username,password,message,search_keywords):
	L = LinkedInScrapper(username,password,message,search_keywords)
	L.Login()
	L.Search()
	while True:
		L.send_notes()
		L.nextPage()

if __name__ == "__main__":
	#Call the function

	user_name = user
	user_password = password
	user_message = message
	user_search_keywords = keyword
	main(user_name,user_password,user_message,user_search_keywords)
