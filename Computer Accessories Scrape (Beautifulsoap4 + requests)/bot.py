import requests
from bs4 import BeautifulSoup
import re, csv

def get_products_link(url):
    links = set()
    i = 1
    while True:
        link_set_temp = set()
        url_next = url + "?page=" + str(i)
        try:
            response = requests.get(url_next)
        except:
            continue

        soup = BeautifulSoup(response.content,"html.parser")

        div_content = soup.find("div", {"id": "content"})

        for link in div_content.findAll('a', attrs={'href': re.compile("^https://")}):
            l = link.get('href')

            if l.endswith(".html"):
                links.add(l)
                link_set_temp.add(l)

        if len(link_set_temp) == 0:
            break

        i += 1
    input_link = url
    return links, input_link

def save_csv(row, file_name):
    with open(file_name, 'a+', newline='') as csvfile:
        fieldnames = ['Title', 'Price', 'Brand', 'Product Code', 'Availability', 'Link', 'Input Url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(row)

def get_product_infos_and_save(product_links, file_name, input_url):
    for link in product_links:

        infos = {}

        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")

        div_content = soup.find("div", {"class" : "content-product-right col-md-7 col-sm-12 col-xs-12"})
        try:
            title = div_content.find('h1', attrs={'itemprop': 'name'}).text
        except:
            title = "Could not scrape"

        try:
            price = div_content.find('span', attrs={'itemprop': 'price'}).get('content')[:-5]
        except:
            price = "Could not scrape"
        try:
            brand = div_content.find('span', attrs={'itemprop': 'name'}).text.strip()
        except:
            brand = "Could not scrape"

        try:
            product_code = div_content.find("div", attrs={"class": "model"}).text[15:].replace("-", " ")
        except:
            product_code = "Could not scrape"

        try:
            availability = div_content.find("div", attrs={"class": "stock"}).text[15:]
        except:
            availability = "Could not scrape"

        # print("Title : ", title)
        # print("Price : ", price)
        # print("Brand : ", brand)
        # print("Product Code : ", product_code)
        # print("Availability : ", availability)

        infos['Title'] = title
        infos['Price'] = price
        infos['Brand'] = brand
        infos['Product Code'] = product_code
        infos['Availability'] = availability
        infos['Link'] = link
        infos['Input Url'] = input_url

        save_csv(infos, file_name)

if __name__ == "__main__":

    # url = "https://mdcomputers.in/processor"
    # csv_file = "data.csv"

    url = input("Enter link here : ")
    csv_file = input("Enter CSV file name here : ")

    urls = url.split(",")

    for u in urls:
        print("Getting products links...", end="")

        product_links, input_url = get_products_link(u.strip())

        print("Done")
        print(f"Total {len(product_links)} product links scraped.")
        print("Hold on, while I scrape all this products, it might take some times depending on number of products")
        get_product_infos_and_save(product_links, csv_file, input_url)

        print("Completed, please wait for next url, if you have entered multiple urls")
