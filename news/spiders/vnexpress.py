# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class QuotesSpider(scrapy.Spider):
    name = "vnexpress"
    array_cate = [
            {"cate_id":'1001005',"cate_name":"Thời sự"},
            {"cate_id":'1001002',"cate_name":"Thế giới"},
            {"cate_id":'1003159',"cate_name":"Kinh doanh"},
            {"cate_id":'1002691',"cate_name":"Giải trí"},
            {"cate_id":'1002565',"cate_name":"Thể thao"},
            {"cate_id":'1001007',"cate_name":"Pháp luật"},
            {"cate_id":'1003497',"cate_name":"Giáo dục"},
            {"cate_id":'1003750',"cate_name":"Sức khoẻ"},
            {"cate_id":'1002966',"cate_name":"Đời sống"},
            {"cate_id":'1003231',"cate_name":"Du lịch"},
            {"cate_id":'1001009',"cate_name":"Khoa học"},
            {"cate_id":'1002592',"cate_name":"Số hoá"},
            {"cate_id":'1001006',"cate_name":"Xe"},
        ]
    dict_cate = {
        "thoi-su":"Thời sự",
        "the-gioi":"Thế giới",
        "kinh-doanh":"Kinh doanh",
        "giai-tri":"Giải trí",
        "the-thao":"Thể thao",
        "phap-luat":"Pháp luật",
        "giao-duc":"Giáo dục",
        "suc-khoe":"Sức khoẻ",
        "doi-song":"Đời sống",
        "du-lich":"Du lịch",
        "khoa-hoc":"Khoa học",
        "so-hoa":"Số hoá",
        "oto-xe-may":"Xe",
        "bong-da":"Bóng đá"
    }
    cate = ""
    def start_requests(self):
        to_time_stamp = int(time.time())
        duration_day = 86400
        duration_month = duration_day*30
        from_time_stamp = to_time_stamp - duration_day*365
        for x in self.array_cate:
            url = 'https://vnexpress.net/category/day?cateid='+x['cate_id']+'&fromdate='+str(from_time_stamp)+'&todate='+str(to_time_stamp)+'&allcate='+x['cate_id']+'||'
            # self.item.update({"category":x['cate_name']})
            yield Request(url, self.parse)

    def parse(self, response):
        next_url = response.css('a.next::attr(href)').get()
        list_url_news = response.css('article.list_news h3.title_news a::attr(href)').getall()
        for x in list_url_news:
            if(('video' not in x and "infographics" not in x and "longform" not in x)):
                yield Request(x, self.save_data)
        if (next_url):
            yield Request('https://vnexpress.net'+next_url,self.parse)

    def save_data(self, response): 
        item = {}
        title = response.css('h1.title_news_detail::text').get()
        description = response.xpath('//*[@class="description"]/text()').extract()[0]

        em = ' '.join(response.css('p.Normal em::text').getall())
        subtitle = ' '.join(response.css('p.subtitle strong::text').getall())
        content = ' '.join(response.css('p.Normal::text').getall())
        content = em + subtitle + content
        time = response.css('header.clearfix span.time::text').get()
        author =  response.css('p.author_mail strong::text').get() 
        if not author:
            author = ' '.join(response.xpath('//p[@class="Normal"]/strong/text()').extract()[-1])
        if not author:
            author=''
        category = response.request.url.split('/')[3]
        category = self.dict_cate[category]
        if('content'!=''):
            item.update({
                "category":category,
                "url":response.url,
                "title":title,
                "description":description,
                "content":content,
                "time":time,
                "author":author
            })
            yield item

