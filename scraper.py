from sys import stderr
from math import log10
import os 
import time
import re

from unidecode import unidecode

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class Crawler():
	main_url = 'https://jobinja.ir/'

	def init_selenium(self):
		options = FirefoxOptions()
		options.add_argument("--headless")
		self.driver = webdriver.Firefox(options=options)
		self.driver.implicitly_wait(5)

	def end_selenium(self):
		self.driver.quit()

	def submit_query(self):
		query = input("what do you want to search for:")
		self.main_url = f"https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B%5D={query}&filters%5Blocations%5D%5B%5D=%D8%AA%D9%87%D8%B1%D8%A7%D9%86&filters%5Bjob_categories%5D%5B%5D=%D9%88%D8%A8%D8%8C%E2%80%8C+%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87%E2%80%8C%D9%86%D9%88%DB%8C%D8%B3%DB%8C+%D9%88+%D9%86%D8%B1%D9%85%E2%80%8C%D8%A7%D9%81%D8%B2%D8%A7%D8%B1&page="


	def get_page_content(self, url):
		self.driver.get(url)
		return self.driver.page_source


	def get_jobs_list(self):
		listt = []
		url = self.main_url + str(1)
		content = self.get_page_content(url)
		soup = BeautifulSoup(content, 'html.parser')
		text = soup.find_all(class_="c-jobSearchState__numberOfResultsEcho")[0].string
		num_farsi = re.findall(r'[۰۱۲۳۴۵۶۷۸۹]+', str(text)) 
		num_page = int(unidecode(num_farsi[0]))
		for i in range(num_page):
			print(i+1)
			url = self.main_url + str(i+1)
			content = self.get_page_content(url)
			soup = BeautifulSoup(content, 'html.parser')
			Jobs = soup.find_all(class_="c-jobListView__titleLink")
			for Job in Jobs:
				if self.check_background_for_jobs_list(Job['href']):
					listt.append(Job['href'])
					with open('list.txt', 'a+') as f:
						f.write("%s\n" % Job['href'])


	def check_background_for_jobs_list(self, link):
		content = self.get_page_content(link)
		soup = BeautifulSoup(content, 'html.parser')
		job_background = soup.select(".black")
		if job_background[3].text == "مهم نیست":
			return True
		else:
			return False
		


	

spider = Crawler()
spider.submit_query()
spider.init_selenium()
spider.get_jobs_list()
spider.end_selenium()

