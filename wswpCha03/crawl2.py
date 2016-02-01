from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
baseUrl = "http://en.wikipedia.org"
baseUrl = "http://home.fnal.gov/~perdue/"

httpString = r"^http"

regexString = r"^(/wiki/)"
regexString = r""


def getLinks(pageUrl):
    global pages
    newUrl = baseUrl + pageUrl
    print(newUrl)
    html = urlopen(newUrl)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll("a", href=re.compile(regexString)):
        if link.attrs["href"] not in pages:
            newPage = link.attrs["href"]
            if not re.search(r"html$", newPage):
                continue
            pages.add(newPage)
            # don't follow mail liks
            if re.search(r"^mailto", newPage):
                continue
            # Only follow relative links
            if not re.search("^http", newPage):
                getLinks(newPage)

getLinks("")
