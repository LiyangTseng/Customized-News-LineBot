import requests
from bs4 import BeautifulSoup

def crawl():
    url = "https://www.cnbc.com/patti-domm/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # focus on crawling CNBC week summary
    targets = soup.find_all("div", class_="RiverCard-standardBreakerCard RiverCard-specialReportsRiver RiverCard-card")
    for target in targets:
        # exclude premium content
        if target.find_all("div", "RiverCard-pro"):
            continue
        # get news title and link
        title = target.find("a", "RiverCard-title").text
        link = target.find("a", "RiverCard-title").get("href")
        print(title)
        print(link)

if __name__ == "__main__":
    
    crawl()