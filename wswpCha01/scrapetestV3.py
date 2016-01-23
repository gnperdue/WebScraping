from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://pythonscraping.com/pages/page1.html")
bsObj = BeautifulSoup(html.read())
print(bsObj.h1)
print(bsObj.html.body.h1)
print(bsObj.body.h1)
print(bsObj.html.h1)
