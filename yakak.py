#Kayak flight price scraper and reminder
import requests, bs4, os, re
import urllib.request
import shutil

url = "https://www.kayak.com/flights/PIT-DEN/2017-04-19/2017-04-26"

#url = "https://www.kayak.com/flights/" + startAirport + "-" + endAirport + "/" + startDate + "/" + endDate

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

res = requests.get(url, headers=headers)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')

pricePanel = soup.select("#searchResultsList")

print(str(pricePanel))
