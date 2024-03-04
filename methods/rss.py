import requests as r
from bs4 import BeautifulSoup

def getArticleIds(urls: list[str]) -> list[int]:
    articleList = []
    for url in urls:
        res = r.get(url).text
        soup = BeautifulSoup(res, "xml")
        items = soup.find("channel")
        for item in items:
            guid = item.find("guid")
            if guid is not None:
                articleList.append(int(guid.text.split(":")[3]))
    articleList.sort()
    return list(dict.fromkeys(articleList))

