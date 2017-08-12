# amazoncrawler - Crawls bestsellers in books on Amazon India and US websites.

Description
-----------------
Web crawler written using Scrapy. It compiles the bestsellers in a single csv file. Domain usage depends on the parameter supplied.
Default domain is `amazon.in`


Installation
-----------------
`pip install scrapy`

Usage
-----------------

To view the items only:
`scrapy crawl amazon [-a country=us ]`

To save the items in a csv file:
`scrapy crawl amazon [-a country=us ] -o $file.csv`

Examples
-----------------
1. `scrapy crawl amazon -o output.csv`

2. `scrapy crawl amazon -a country=us -o output.csv`
