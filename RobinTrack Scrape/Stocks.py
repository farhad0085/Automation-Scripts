from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://robintrack.net/symbol/F")

i = 0
while True:
    driver.find_element_by_css_selector('#root > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > h1 > a').click()