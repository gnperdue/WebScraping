"""
A general crawler example.
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
allExtLinks = set()
allIntLinks = set()
random.seed(datetime.datetime.now())


def getInternalLinks(bsObj, includeUrl):
    """
    Retrieves a list of all internal links found on a page.
    """
    internalLinks = []
    # find all links that begin with a "/"
    for link in bsObj.findAll('a', href=re.compile("^(/|/*" +
                                                   includeUrl + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks


def getExternalLinks(bsObj, excludeUrl):
    """
    Retrieves a list of all external links found on a page.
    """
    externalLinks = []
    # find all links that start with 'http' or 'www' that do not contain the
    # current url.
    hrefregex = re.compile("^(http|www)((?!" + excludeUrl + ").)*$")
    for link in bsObj.findAll('a', href=hrefregex):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts


def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(bsObj, startingPage)
        return getRandomExternalLink(
            internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]


def getNextExternalLink(link):
    pass


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("Random external link is: " + externalLink)
    followExternalOnly(externalLink)


def getAllExternalLinks(siteUrl):
    """
    Collects a list of all external URLs found on the site.
    """
    pass


followExternalOnly("http://oreilly.com")
