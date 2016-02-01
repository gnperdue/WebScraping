# Starting to Crawl

Be conscientious of bandwidth use when crawling.

## Traversing a Single Domain

Let's work on a "Six Degrees of Wikipedia" solution. What is the smallest number
of links that will take us from the "Eric Idle" page to the "Kevin Bacon" page?

We need to be able to filter links we are not interested in. If we examine the
links that point to article pages, they all have three things in common:

* they reside within the `div` and the `id` set to `bodyContent`
* the urls do not comain semicolons
* the urls begin with `/wiki/`

We need to generalize our scripts:

* we need a single function, `getLinks` that takes a Wikipedia article URL of
the form `/wiki/<Article_Name>` and returns a list of all linked article URLs
in the same form.
* a main function that calls `getLinks` with some starting article, chooses
a random article link from the list, and calls `getList` again until we stop
the program or until there are no article links found on the new page

## Crawling an Entire Site

Generally we need access to a database to store results as we crawl. Otherwise,
the process is too memory intensive.

When might we want to crawl a whole site, and when not?

* Generating a site map
* Gathering data

The gneral approach is to start with a top level page, search for all links, and
recursively crawl them. This can get big fast: if a site has 10 links per page
and is five pages deep, there are 10^5 pages we must crawl before we're sure
we've been to them all. Of course, most of these will be duplicates.

To avoid crawling the same page twice, it is important internal links are
discovered and formatted consistently, and kept in a structure for easy look-up.

### Collecting Data Across an Entire Site

In order to make crawlers useful, we need to be able to do something on the
page while we're there. Suppose we want a scraper that collects the title, the
first paragraph of content, and the link to edit the page (if available).

Looking at a few pages, we notice

* All titles (on all pages) have titles under `h1->span` tags, and these are
the only `h1` tags on the page.
* All body text lives under the `div#bodyContent` tag. For just the first
paragraph of text, we want `div#mw-content-text->p`. This is true for all pages
but file pages.
* Edit links occur only on article pages. They will be found under
`li#ca-edit->span->a`.

## Crawling Across the Internet

Before writing a crawler that simply follows outbound links, we need to ask
and/or answer a few questions:

* What data am I trying to gather? Can this be accomplished by scraping just a
few pre-defined websites? Or does my crawler need to be able to discover new
websites I might not know about?
* When the crawler reachs a particular site, will it immediately follow the
next outbound link or will it stick around and drill down into the current
site?
* Are there conditions under which I would not want to scrape a particular site?
Am I interested in non-English content?
* How am I protecting myself against legal action if my web crawler catches the
attention of a webmaster on one of the sites it runs across?

Note: Handling Redirects: Redirects allow the same page to be viewable under
different domain names. Redirects come in two types:

* Server-side, where the URL is changed before the page is loaded
* Client-side, sometimes seen with a "you will be redirected in x seconds"
message, where the page loads before redirecting to the new one.

For server-side redirects, we usually don't have to worry. We'll look at
client-side redirects later.

## Crawling with Scrapy

Scrapy is a Python library that handles much of the complexity of finding and
evaluating links on a website. Unfortunately, it is not available in Python 3
yet (just 2.7). 

At this point, code moves to the `Python2` directory...

    (python2)Python2$ ls
    (python2)Python2$ which scrapy
    /Users/gnperdue/anaconda/envs/python2/bin/scrapy
    (python2)Python2$ scrapy startproject wikiSpider
    2015-09-08 21:29:23 [scrapy] INFO: Scrapy 1.0.3 started (bot: scrapybot)
    2015-09-08 21:29:23 [scrapy] INFO: Optional features available: ssl, http11, boto
    2015-09-08 21:29:23 [scrapy] INFO: Overridden settings: {}
    New Scrapy project 'wikiSpider' created in:
    /Users/gnperdue/Dropbox/Programming/Programming/Python/WebScraping/wswpCha03/Python2/wikiSpider
    
    You can start your first spider with:
    cd wikiSpider
    scrapy genspider example example.com
    (python2)Python2$ tree
    .
    └── wikiSpider
        ├── scrapy.cfg
        └── wikiSpider
            ├── __init__.py
            ├── items.py
            ├── pipelines.py
            ├── settings.py
            └── spiders
                └── __init__.py
    
    3 directories, 6 files

To create a crawler, we add a new file to

    wikiSpider/wikiSpider/spiders/articleSpider.py

called `items.py`. We also define a new item called `Article` inside `items.py`.

Each Scrapy `Item` object represents a single page on the website. We can define
as many fields as we like (`url`, `content`, `header image`, etc.), but we'll
just use `title` in our example.

Update...

    (python2)Python2$ tree
    .
    └── wikiSpider
        ├── scrapy.cfg
        └── wikiSpider
            ├── __init__.py
            ├── items.py
            ├── pipelines.py
            ├── settings.py
            └── spiders
                ├── __init__.py
                ├── articleSpider.py
                ├── articleSpider.py~
                └── items.py
    
    3 directories, 9 files

Go to the main `wikiSpider` directory...

Well...

    (python2)wikiSpider$ ls
    scrapy.cfg  wikiSpider/
    (python2)wikiSpider$ scrapy crawl article
    Traceback (most recent call last):
    File "/Users/gnperdue/anaconda/envs/python2/bin/scrapy", line 6, in <module>
    sys.exit(execute())
    File "/Users/gnperdue/anaconda/envs/python2/lib/python2.7/site-packages/scrapy/cmdline.py", line 142, in execute
    cmd.crawler_process = CrawlerProcess(settings)
    File "/Users/gnperdue/anaconda/envs/python2/lib/python2.7/site-packages/scrapy/crawler.py", line 209, in __init__
    super(CrawlerProcess, self).__init__(settings)
    File "/Users/gnperdue/anaconda/envs/python2/lib/python2.7/site-packages/scrapy/crawler.py", line 115, in __init__
    self.spider_loader = _get_spider_loader(settings)
    File "/Users/gnperdue/anaconda/envs/python2/lib/python2.7/site-packages/scrapy/crawler.py", line 296, in _get_spider_loader
    return loader_cls.from_settings(settings.frozencopy())
    File "/Users/gnperdue/anaconda/envs/python2/lib/python2.7/site-packages/scrapy/spiderloader.py", line 30, in from_settings
    return cls(settings)
    File "/Users/gnperdue/anaconda/envs/python2/lib/python2.7/site-packages/scrapy/spiderloader.py", line 21, in __init__
    for module in walk_modules(name):
    File "/Users/gnperdue/anaconda/envs/python2/lib/python2.7/site-packages/scrapy/utils/misc.py", line 71, in walk_modules
    submod = import_module(fullpath)
    File "/Users/gnperdue/anaconda/envs/python2/lib/python2.7/importlib/__init__.py", line 37, in import_module
    __import__(name)
    File "/Users/gnperdue/Dropbox/Programming/Programming/Python/WebScraping/wswpCha03/Python2/wikiSpider/wikiSpider/spiders/articleSpider.py", line 3, in <module>
    from wikiSpider.items import Article
    ImportError: cannot import name Article

Re-org a bit...

    (python2)wikiSpider$ ls
    scrapy.cfg  wikiSpider/
    (python2)wikiSpider$ tree
    .
    ├── scrapy.cfg
    └── wikiSpider
        ├── __init__.py
        ├── items.py
        ├── pipelines.py
        ├── settings.py
        └── spiders
            ├── __init__.py
            ├── articleSpider.py
            └── articleSpider.py~
    
    2 directories, 8 files

Try again... Better, but still need to do some yak-shaving:

    (python2)wikiSpider$ scrapy crawl article
    2015-09-08 21:47:12 [scrapy] INFO: Scrapy 1.0.3 started (bot: wikiSpider)
    2015-09-08 21:47:12 [scrapy] INFO: Optional features available: ssl, http11, boto
    2015-09-08 21:47:12 [scrapy] INFO: Overridden settings: {'NEWSPIDER_MODULE': 'wikiSpider.spiders', 'SPIDER_MODULES': ['wikiSpider.spiders'], 'BOT_NAME': 'wikiSpider'}
    2015-09-08 21:47:12 [py.warnings] WARNING: :0: UserWarning: You do not have a working installation of the service_identity module: 'No module named service_identity'.  Please install it from <https://pypi.python.org/pypi/service_identity> and make sure all of its dependencies are satisfied.  Without the service_identity module and a recent enough pyOpenSSL to support it, Twisted can perform only rudimentary TLS client hostname verification.  Many valid certificate/hostname mappings may be rejected.

    ...
    AttributeError: 'NoneType' object has no attribute '_app_data'
    2015-09-08 21:47:21 [scrapy] DEBUG: Crawled (200) <GET https://en.wikipedia.org/wiki/Main_Page> (referer: None)
    Title is: Main Page
    2015-09-08 21:47:21 [scrapy] DEBUG: Scraped from <200 https://en.wikipedia.org/wiki/Main_Page>
    {'title': u'Main Page'}

Okay, well, something.
