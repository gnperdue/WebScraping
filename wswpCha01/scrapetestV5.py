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


if html is None:
    print("URL not found")
else:
    print("URL okay")
    # program may continue

bsObj = BeautifulSoup(html.read())
print(bsObj.h1)
print(bsObj.html.body.h1)
print(bsObj.body.h1)
print(bsObj.html.h1)

try:
    badContent = bsObj.nonExistingTag.anotherTag
except AttributeError as e:
    print("Crazy tag you made up was not found...")
else:
    if badContent is None:
        print("Tag wasn't present, but no exception.")
    else:
        print(badContent)
