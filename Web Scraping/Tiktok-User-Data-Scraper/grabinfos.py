'''
I am really sorry that i disappoint you.
Last night i wrote an script which scraped almost 150+ users profile.
It was only for test purpose. So i didn't try with a large amount you know.
But after that they (tiktok) blocked my request.
Now I can't access the website.
I tried using proxy but no output. So I give up.
'''

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from websiteslinks import LinkHelper
import re
import csv

lh = LinkHelper()
totalLink = lh.linkNumber()

i = 1

driver = webdriver.Firefox()
driver.set_page_load_timeout(1000)  # 1000 seconds

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

while i<=totalLink:

    url = lh.readExactLink(i)
    driver.get(url)
    time.sleep(1)

    file = open("data.txt", 'a+')

    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        linksssss = elem.get_attribute("href")

        if linksssss.startswith("https://www.tiktok.com/@"):
            file.write(linksssss + "\n")

    address = driver.find_element_by_xpath("//meta[@name='description']").get_attribute('content')

    #handling page not found
    if address.startswith("TikTok"):
        i += 1
        continue

    # removing emojis from text
    address = deEmojify(address)

    # find first @
    at = address.find("@")
    # get first half
    username = address[:at]
    uName = re.sub('\W+', ' ', username)
    fh = re.sub('\W+', ' ', username).split()

    username = address.split()[0]
    userid = address.split()[1 + len(fh) - 1]
    userid = re.sub('\W+', '', userid)

    likes = address.split()[5 + len(fh) - 1]
    follower = address.split()[7 + len(fh) - 1]

    data = []

    data.append(uName.strip())
    data.append(userid)
    data.append(likes)
    data.append(follower)

    print(data)

    f = open('users.csv', 'a+')

    with f:
        writer = csv.writer(f)
        writer.writerow(data)

    print("Added " + str(i)+ " items to csv!")

    i += 1

time.sleep(10)
driver.quit()