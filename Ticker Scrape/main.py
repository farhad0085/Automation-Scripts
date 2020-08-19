import requests
from bs4 import BeautifulSoup
import random
import datetime
import pandas as pd

def get_page_source(url):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    ]

    user_agent = random.choice(user_agents)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": user_agent
    }

    # response_content = requests.get(url, headers=headers).text
    response_content = open("page_source.html", "r").read()
    return response_content

def get_ticker_input():
    # ticker = input("Enter Ticker: ")
    ticker = "aapl"
    ticker = ticker.lower()
    return ticker

def get_page_url(ticker):
    page = "https://finviz.com/quote.ashx?t="
    final_link = page + ticker
    return final_link

def get_soup(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    return soup

def get_financial_data(soup, ticker):
    table = soup.find("table", class_="snapshot-table2")

    trs = table.find_all("tr")

    output_data = []
    row_dict = {}
    row_dict["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:S")
    row_dict["ticker"] = ticker
    for tr in trs:
        tds = tr.find_all("td")
        i = 0
        while i < len(tds):
            if i % 2:
                row_dict[tds[i-1].text] = tds[i].text   
            i += 1
    output_data.append(row_dict)
    return output_data

def get_analysts_outlook_data(soup):
    table = soup.find("table", class_="fullview-ratings-outer")
    tables = table.find_all("table")

    output_data = []
    for table in tables:
        row_dict = {}
        tr = table.find("tr")
        tds = tr.find_all("td")
        row_dict["date"] = tds[0].text
        row_dict["second"] = tds[1].text
        row_dict["third"] = tds[2].text
        row_dict["fourth"] = tds[3].text
        row_dict["fifth"] = tds[4].text
        output_data.append(row_dict)
    
    return output_data

def get_trading_data(soup):
    table = soup.find("table", class_="body-table")
    trs = table.find_all('tr')

    output_data = []
    for index, tr in enumerate(trs):
        if index == 0:
            continue
        row_dict = {}

        tds = tr.find_all('td')
        row_dict['insider_trading'] = tds[0].text
        row_dict['relationship'] = tds[1].text
        row_dict['date'] = tds[2].text
        row_dict['transaction'] = tds[3].text
        row_dict['cost'] = tds[4].text
        row_dict['shares'] = tds[5].text
        row_dict['value'] = tds[6].text
        row_dict['total_share'] = tds[7].text
        row_dict['sec_form_four'] = tds[8].text
        output_data.append(row_dict)

    return output_data

def main():
    ticker = get_ticker_input()
    page_url = get_page_url(ticker)
    page_source = get_page_source(page_url)
    soup = get_soup(page_source)

    # financial_data = get_financial_data(soup, ticker)
    # df_financial = pd.DataFrame(financial_data)
    # df_financial.to_html("Financial.html")

    # analysis_outlook_data = get_analysts_outlook_data(soup)
    # df_analysis_outlook = pd.DataFrame(analysis_outlook_data)
    # df_analysis_outlook.to_html("Analysis_Outlook.html")

    trading_data = get_trading_data(soup)
    df_trading = pd.DataFrame(trading_data)
    df_trading.to_html("Trading.html")

if __name__ == "__main__":
    main()
    