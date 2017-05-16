# - * - coding: utf-8 - * -

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from BookSpider.items import BookspiderItem
import re,sys
reload(sys)
sys.setdefaultencoding('utf8')

class DouBan(CrawlSpider):
    name = 'Book'
    start_urls = ['https://book.douban.com/top250']
    redis_key = "DoubanSpider:start_urls"
    download_delay = 1

    def parse(self, response):
        selector = Selector(response)
        book_urls = selector.xpath("//tr[@class='item']/td[2]/div[@class='pl2']/a/@href").extract()

        for book in book_urls:
            yield Request(book,callback=self.parse_books)

        nextLink = selector.xpath("//span[contains(@class, 'next')]/a/@href").extract()
        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield Request(nextLink,callback=self.parse)

    def parse_books(self, response):
        item = BookspiderItem()
        selector = Selector(response)
        bookid = str(re.search('subject/(.*?)/',response.url).group(1))
        title = selector.xpath('//h1/span/text()').extract()
        author = selector.xpath("//div[@id='info']/a[1]/text()").extract()
        author = author[0].replace(' ','').replace('\n','')

        info = selector.xpath("//div[@id='info']").extract()
        info = ''.join(info).replace(' ','').replace('\n','')
        info = info.decode('utf-8')

        isbn13 = str(re.search('ISBN:</span>(.*?)<br>',info).group(1))
        publisher =str(re.search(u'\u51fa\u7248\u793e:</span>(.*?)<br>',info).group(1))
        pubdate = str(re.search(u'\u51fa\u7248\u5e74:</span>(.*?)<br>',info).group(1))
        price = str(re.search(u'\u5b9a\u4ef7:</span>(.*?)<br>',info).group(1))
        pages = str(re.search(u'\u9875\u6570:</span>(.*?)<br>',info).group(1))
        translator = re.search(u'\u8bd1\u8005:</span>(.*?)<br>', info)
        if translator :
            translator = str(re.search(u'>(.*?)</a>', translator.group(1)).group(1))
        summary = selector.xpath("//div[@class='intro']/p/text()").extract()
        #catalog =
        lookcount = selector.xpath("//div[@id='collector']/p[contains(@class, 'pl')][2]/a/text()").extract()
        lookcount = ''.join(lookcount)
        lookcount = str(re.search(u'(\d+)',lookcount).group(1))
        image = response.xpath("//a[@class = 'nbg']/img/@src").extract()

        item['bookid'] = bookid
        item['title'] = title
        item['author'] = author
        item['image'] = image


        item['isbn13'] = isbn13
        item['publisher'] = publisher
        item['pubdate'] = pubdate
        item['price'] = price
        item['pages'] = pages
        if translator:
            item['translator'] = translator
        item['summary'] = summary
        #item['catalog'] = catalog
        item['lookcount'] = lookcount

        yield item