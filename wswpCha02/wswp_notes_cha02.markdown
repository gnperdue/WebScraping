# Advanced HTML Parsing

## You Don't Always Need a Hammer

Tricks to avoid complicated lines:

* look for a "print this page" link or a mobile version that has better formatted
HTML
* look for info hidden in a JavaScript file
* info might be avaialble in the url of the page itself
* are there other sources for the information?

## Another Serving of BeautifulSoup

We'll search tags by attributes, work with lists of tags, and parse tree
navigation.

Note: `.get_text()` strips all tages from the document we're working with and
returns a string containing the text only. But remember that it is much easier
to find things in a BeautifulSoup object than in a block of text. Calling
`.get_text()` should be the "last" thing we do (before printing, etc.).

### `find()` and `findAll()` with BeautifulSoup

`find()` and `findAll()` are workhorses.

    findAll(tag, attributes, recursive, text, limit, keyword)
    find(tag, attributes, recursive, text, keyword)

The arguments:

* `tag` may be a string or a list of strings (or a set?)

        .findAll({"h1", "h2"})   # etc.

* `attributes` takes a dictionary

        .findAll("span", {"class": {"green", "red"}})

* `recursive` takes a boolean (`findAll` default is `True`)
* `text` matches based on the text content of the tags rather than the properties

        nameList = bsObj.findAll(text="the prince")
        print(len(nameList))

* `limit` is only used in `findAll` - note that it gives items in the order they
occur on the page
* `keyword` lets us select tags with particular attributes

Not: `keyword` is technically redundant. The following are equivalent:

    bsObj.findAll(id="text")
    bsObj.findAll("", {"id": "text"})

We must also be careful searching by `class` since that is a protected word in
Python. So

    bsObj.findAll(class="green")

will produce a syntax error. BeautifulSoup's solution is to add an underscore:

    bsObj.findAll(class="green")

But we may also put the `class` in quotes:

    bsObj.findAll("", {"class": "green"})

My `find()` function references doesn't even show `keyword`:

    find(name = None, attrs = {}, recursive = True, text = None, **kwargs)

Nominally, the `keyword` argument allows to take the "or" structure of the
`attributes` argument and apply an "and" filter to it.

### Other BeautifulSoup Objects

* `BeautifulSoup` objects
* `Tag` objects, e.g., `bsObj.div.h1`
* `NavigableString` objects - used to represent text within tags
* `Comment` objects

### Naviagting Trees

What if we need to find a tag based on location? This is where tree navigation
comes in handy.

    bsObj.tag.subTag.anotherSubTag

#### Dealing with children and other descendants

In BeautifulSoup, there is a distinction between _children_ and _descendants_.
Children are alway exactly one tag below a parent, while descendants can be at
any level in the tree below a parent.

In general, BeautifulSoup functions will always deal with the descendants of
the current selected tag. `bsObj.body.h1` selects the first `h1` tag that is
a descendant of the `body` tag. It won't find tags outside of the body.
`bsObj.div.findAll("img")` will find the first `div` tag in the doc and then
retrieve a list of all `img` tags that are its descendants. To find only
descendants that are children, use the `.children` tag.

#### Dealing with siblings

`next_siblings()` makes it easy to collect data from tables, especially those
with title rows.

    for sibling in bsObj.find("table", {"id": "giftList"}).tr.next_siblings:
        print(sibling)

We get all the rows of products from the product table except for the first
title row. As a complement to `next_siblings()`, `previous_siblings()` can
often be helpful if there is an easily selectable tag at the end of a list
of sibling tags that you would like.

There are also the `next_sibling()` and `previous_sibling()` functions.

#### Dealing with your parents

`BeautifulSoup` has `.parent` and `.parents` functions, although we will use them
less than the sibling and children accessors.

    print(bsObj.find("img", {"src": "../img/gifts/img1.jpg"}
                     ).parent.previous_sibling.get_text())

## Regular Expressions

A classic regex application is looking for email addresses.

1. at least one of: uppercase letters, lowercase letters, the numbers 0-9,
periods, plus signs, or underscores

        [A-Za-z0-9\._+]+

2. then the `@` symbol

        @

3. then at least one uppercase or lowercase letter

        [A-Za-z]+

4. then a period

        \.

5. then `.com`, `.org`, `.edu`, `.net` (or others)

        (com|org|edu|net)

This combines to

    [A-Za-z\._+]+@[A-Za-z]+\.(com|org|edu|net)

Common items in regular expressions:

* `*` preceding character or subexpression 0 or more times
* `+` preceding character or subexpression 1 or more times
* `[]` match any character in the brackets
* `()` grouped subexpression
* `{m,n}` match the previous character or subexpression between `m` and `n`
times
* `[^]` match any character that is _not_ in the brackets
* `|` match `or`
* `.` match any single character
* `^` indicates that a character or subexpression occurs at the beginning of a
string
* `\` escape character
* `$` match to the end of a string
* `?!` "does not contain"

## Regular Expressions and BeautifulSoup

In BeautifulSoup, most functions that take a string can take a regular
expression just as well.

Suppose a page has many images with the following form:

    <img src="../img/gifts/img3.jpg">

We might grab all the image tags using `.findAll("img")`, but we might also
prefer something more robust against unexpected images in the page. We can use
a regex:

    images = bsObj.findAll("img",
        {"src": re.compile("\.\.\/img\/gifts\/img.*\.jpg")})

## Accessing Attributes

Often when scraping we aren't looking for the contents of a tag, we're looking
for its attributes. We can get a dictionary with

    myTag.attrs

This returns a Python dictionary, so we can say, e.g.:

    myImgTag.attrs['src']

## Lambda Expressions

A lambda expression is a function that is passed into another function as a
variable. BeautifulSoup allows us to pass certain types of functions as
parameters into the `findAll` function. They must take a tag object as an
argument and return a boolean. For example:

    soup.findAll(lambda tag: len(tag.attrs) == 2)

## Beyond BeautifulSoup

Other options to check out:

* `lxml`
* HTML Parser - Python's built-in parsing library
