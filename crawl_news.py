import requests
from bs4 import BeautifulSoup
import pyshorteners

class Base_Crawler():
    def __init__(self, web_url):
        self.response = requests.get(web_url)
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def crawl(self, news_num):
        pass

class CNBC_Crawler(Base_Crawler):
    """ crawl week summary (and other news) published by Patti Domm from CNBC """
    def __init__(self, web_url="https://www.cnbc.com/patti-domm/"):
        super(CNBC_Crawler, self).__init__(web_url)
        self.name = "CNBC"
        # observed from the source code of the website
        self.targets = self.soup.find_all("div", class_="RiverCard-standardBreakerCard RiverCard-specialReportsRiver RiverCard-card")

    def crawl(self, N):
        """ return lastest n news  """
        targets = self.soup.find_all("div", class_="RiverCard-standardBreakerCard RiverCard-specialReportsRiver RiverCard-card")
        self.titles_links = []
        for target in targets:
            # exclude premium content
            if target.find_all("div", "RiverCard-pro"):
                continue
            link = target.find("a", "RiverCard-title").get("href")
            date = link.split("https://www.cnbc.com/")[1][:10]
            link = pyshorteners.Shortener().tinyurl.short(link)
            title = "[{date}] {news_title}".format(date=date, 
                                                    news_title=target.find("a", "RiverCard-title").text)
            
            self.titles_links.append((title, link))
            
        return self.titles_links[:N]

# TODO: add more crawlers for other news sources

if __name__ == "__main__":
    c = CNBC_Crawler()
    title_link_pairs = c.crawl(3)
    for title, link in title_link_pairs:
        print(title)
        print(link)