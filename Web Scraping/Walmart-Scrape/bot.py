import os
import time
from selenium import webdriver
import csv
import requests
import secrets
from links_handler import LinkHelper
import re

l = LinkHelper()
total_products = l.linkNumber()

driver = webdriver.Firefox()
driver.set_page_load_timeout(1000)  # 1000 seconds

i = 1

while i <= 25:

	url = l.readExactLink(i)

	driver.get(url)

	time.sleep(1)

	p_name = driver.find_element_by_css_selector(".css-1c6krh5").get_attribute('textContent')
	p_price = driver.find_element_by_css_selector(".css-rykmet > span:nth-child(1)").get_attribute('textContent')
	p_rating = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div/div[1]/div[3]/div[2]/div/div[1]/div/div[1]/div/div[1]/div").get_attribute('width')
	p_rating = round(((float(re.findall(r'\d*\.?\d+', p_rating)[0]))/100)*5, 1) # convert percentage to scale of 5
	p_desc = driver.find_element_by_css_selector(".css-gur09u").get_attribute('textContent')

	# p_neutri = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div/div/div[2]/div[4]/div/section[3]/div[2]").get_attribute('textContent')
	# p_neutri = p_neutri.replace('See Term of Use for more details. For up to date information on products, please speak to the manufacturer.', '')
	# p_neutri = p_neutri.strip()

	data = []

	data.append(p_name)
	data.append(p_price)
	data.append(p_rating)
	data.append(p_desc)
	#data.append(p_neutri)

	print(data)

	f = open('data.csv', 'a+')

	with f:
	    writer = csv.writer(f)
	    writer.writerow(data)

	print("items added to csv!")

	i += 1

driver.quit()