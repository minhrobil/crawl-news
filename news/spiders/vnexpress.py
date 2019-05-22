import scrapy
from scrapy import Request
import re
import time


class QuotesSpider(scrapy.Spider):
    name = "vnexpress"

    def start_requests(self):
        to_time_stamp = int(time.time())
        array_cateid = ['1001005','1001002','1003159','1002691','1002565','1001007']
        duration_day = 86400
        duration_month = duration_day*30
        from_time_stamp = to_time_stamp - 86400
        for x in array_cateid:
            url = 'https://vnexpress.net/category/day?cateid='+x+'&fromdate='+str(from_time_stamp)+'&todate='+str(to_time_stamp)+'&allcate='+x+'||'
            yield Request(url, self.parse)

    def parse(self, response):
        next_url = 'https://vnexpress.net'+response.css('a.next::attr(href)').get()
        list_url_news = response.css('article.list_news h3.title_news a::attr(href)').getall()
        for x in list_url_news:
            yield Request(x, self.save_data)
        if next_url:
            yield Request(next_url,self.parse)

    def save_data(self, response): 
        title = response.css('h1.title_news_detail::text').get()
        description = response.css('p.description::text').get()
        em = ' '.join(response.css('p.Normal em::text').getall())
        subtitle = ' '.join(response.css('p.subtitle strong::text').getall())
        content = ' '.join(response.css('p.Normal::text').getall())
        content = em + subtitle + content
        time = response.css('header.clearfix span.time::text').get()
        author =  response.css('p.author_mail strong::text').get()
        item = {}
        item.update({
            "url":response.url,
            "title":title,
            "description":description,
            "content":content,
            "time":time,
            "author":author
        })
        yield item

