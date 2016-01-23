# Your First Web Scraper

## Connecting

A first test:

    wswpCha01$ which python
    /Users/perdue/anaconda/bin/python
    wswpCha01$ python --version
    Python 3.4.3 :: Anaconda 2.2.0 (x86_64)
    wswpCha01$ python scrapetest.py
    b'<html>\n<head>\n<title>A Useful Page</title>\n</head>\n<body>\n<h1>An Interesting Title</h1>\n<div>\nLorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n</div>\n</body>\n</html>\n'
    wswpCha01$ more scrapetest.py
    from urllib.request import urlopen
    
    html = urlopen("http://pythonscraping.com/pages/page1.html")
    print(html.read())

`urllib` is a standard Python library.

## An Introduction to BeautifulSoup

### Installing BeautifulSoup

We need to use `pip`? - No, we already have it installed with `conda` as part of the base
Anaconda install.

### Running BeautifulSoup

    wswpCha01$ python scrapetestV2.py
    <h1>An Interesting Title</h1>
    wswpCha01$ more scrapetestV2.py
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    
    html = urlopen("http://pythonscraping.com/pages/page1.html")
    bsObj = BeautifulSoup(html.read())
    print(bsObj.h1)

There is some interesting flexibility in getting at the structure of the
BeautifulSoup object.

    wswpCha01$ more scrapetestV3.py
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    
    html = urlopen("http://pythonscraping.com/pages/page1.html")
    bsObj = BeautifulSoup(html.read())
    print(bsObj.h1)
    print(bsObj.html.body.h1)
    print(bsObj.body.h1)
    print(bsObj.html.h1)
    wswpCha01$ python scrapetestV3.py
    <h1>An Interesting Title</h1>
    <h1>An Interesting Title</h1>
    <h1>An Interesting Title</h1>
    <h1>An Interesting Title</h1>

### Connecting Reliably

Consider:

    html = urlopen("http://pythonscraping.com/pages/page1.html")

There are two main things that can go wrong here:

* the page is not found on the server
* the server is not found

We can try to handle this with exceptions:

    try:
        html = urlopen("http://pythonscraping.com/pages/page1.html")
    except HTTPError as e:
        print(e)
        # return null, break, or some other "plan B"
    else:
        # the program continues
        print("ok")

If the server is not found at all, `urlopen` returns `None`.

    if html is None:
        print("URL not found")
    else:
        print("URL okay")
        # program may continue

We also may be missing tags we expect.

    wswpCha01$ python scrapetestV5.py
    ok
    URL okay
    <h1>An Interesting Title</h1>
    <h1>An Interesting Title</h1>
    <h1>An Interesting Title</h1>
    <h1>An Interesting Title</h1>
    /Users/perdue/anaconda/lib/python3.4/site-packages/bs4/element.py:944: UserWarning: .nonExistingTag is deprecated, use .find("nonExisting") instead.
    tag_name, tag_name))
    Crazy tag you made up was not found...

Re-org the code a bit...

    wswpCha01$ python scrapetestV6.py
    <h1>An Interesting Title</h1>

Remember to check exceptions and handle errors. The web is a mess.


