# Tangie library
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

# function for gathering headlines


def fetch_headlines():
    news_url = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en"
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()

    soup_page = soup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    # Print news title, url and publish date
    # for news in news_list:
        # print(news.title.text)
        # print(news.link.text)
        # print(news.pubDate.text)
        #print("-" * 60)
    return news_list
