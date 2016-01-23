from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen("http://pythonscraping.com/pages/page1.html")
except HTTPError as e:
    print(e)
    # return null, break, or some other "plan B"
else:
    # the program continues
    print("ok")


bsObj = BeautifulSoup(html.read())
print(bsObj.h1)
print(bsObj.html.body.h1)
print(bsObj.body.h1)
print(bsObj.html.h1)
