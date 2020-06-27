import os
import time
from selenium import webdriver
import csv
import requests
import secrets
from links_handler import LinkHelper

l = LinkHelper()
total_products = l.linkNumber()

driver = webdriver.Firefox()
driver.set_page_load_timeout(1000)  # 1000 seconds

i = 1

while i <= total_products:
	url = l.readExactLink(i)
	driver.get(url)

	time.sleep(1)

	try:
		p_name = driver.find_element_by_css_selector(".GrE04").get_attribute('textContent')
		p_price = driver.find_element_by_css_selector(".IyLvo").get_attribute('textContent')
		image_link = driver.find_element_by_css_selector("div._2FbOx:nth-child(1) > img:nth-child(1)").get_attribute('src')
													
		# save the image
		page = requests.get(image_link)
		f_ext = os.path.splitext(image_link)[-1]
		f_name = 'images/img_'+secrets.token_hex(16)+f_ext
		with open(f_name, 'wb') as f:
			f.write(page.content)
		    											
		p_d1_title = driver.find_element_by_css_selector("#about_0 > div:nth-child(1) > span:nth-child(1)").get_attribute('textContent')
		p_d1_text = driver.find_element_by_css_selector("#about_0 > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)").get_attribute('textContent')


		p_desc = p_d1_title + " : " + p_d1_text.strip()
		
		data = []

		data.append(p_name)
		data.append(p_price)
		data.append(f_name)
		data.append(p_desc)

		print(data)

		f = open('data.csv', 'a+')

		with f:
		    writer = csv.writer(f)
		    writer.writerow(data)

		print("items added to csv!")
	except:
		print("Something went wrong, Skipping this product")
	
	i += 1

time.sleep(10)
driver.quit()