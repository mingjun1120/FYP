import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

'''
References:
https://stackoverflow.com/questions/44527996/scrapy-understanding-crawlspider-and-linkextractor
https://docs.scrapy.org/en/latest/topics/link-extractors.html
https://docs.scrapy.org/en/latest/topics/selectors.html
https://stackoverflow.com/questions/9012008/pythons-re-return-true-if-string-contains-regex-pattern
scrapy shell "http://quotes.toscrape.com/page/1/"
'''

with open('URL_Regex.txt') as f:
    for count, x in enumerate(f.readlines()):
        if count == 0:
            regexCreatedIndex = x.replace('\n', '')
        elif count == 1:
            firstBackUrlIndex = x.replace('\n', '')
        elif count == 2:
            regexCreatedThread = x.replace('\n', '')
        elif count == 3:
            firstBackUrlThread = x.replace('\n', '')
        elif count == 4:
            regexCreatedPageFlip = x.replace('\n', '')
        else:
            firstBackUrlPageFlip = x.replace('\n', '')


class ForumcrawlerSpider(CrawlSpider):
    name = 'ForumCrawler'
    allowed_domains = ['namepros.com']
    start_urls = ['https://www.namepros.com/']

    rules = (Rule(LinkExtractor(tags='a', allow=(regexCreatedIndex[1:-1],)), callback='parse_item', follow=True),)

    def parse_item(self, response):

        # response.xpath("//a[@href]/@href").getall()

        # Create empty lists
        pageFlipUrls = []
        indexUrls = []
        threadUrls = []

        # [1:-1] is to remove the ^ symbol at the beginning and $ symbol at the end of the string
        if re.compile(regexCreatedPageFlip[1:-1]).search(response.url):
            pageFlipUrls.append(response.url)

        elif re.compile(f'{firstBackUrlIndex}\/{regexCreatedIndex[1:-1]}').search(response.url):
            indexUrls.append(response.url)

        elif re.compile(f'{firstBackUrlThread}\/{regexCreatedThread[1:-1]}').search(response.url):
            threadUrls.append(response.url)
        else:
            pass

        for count, urlType in enumerate([indexUrls, threadUrls, pageFlipUrls]):
            for url in urlType:
                if count == 0:
                    urlType = 'INDEX'
                elif count == 1:
                    urlType = 'THREADS'
                else:
                    urlType = 'PAGE-FLIP'
                yield {
                    'URL Type': urlType,
                    'URL': url
                }

