# -*- coding: utf-8 -*-
import scrapy
import re
from comments.spiders.helper import getTid
from comments.items import CommentsItem

class HubeiSpider(scrapy.Spider):
    name = 'hubei'
    allowed_domains = ['liuyan.people.com.cn']
    start_urls = ['http://liuyan.people.com.cn/forum/list?fid=28']
    domainName = ['医疗']

    # Store leaders' ID
    fidList = []
    cityNums = 0


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.getProvinceFid)

    def getProvinceFid(self, response):
        # Links of province leaders' comment
        leaderUrlList = response.xpath('//a[@class="message_index"]/@href').getall()
        for leaderUrl in leaderUrlList:
            self.fidList.append(leaderUrl.split('=')[-1])
        
        # Links of cities
        UrlList = response.xpath('//a[@class="count-limit"]/@href').getall()
        forumUrlList = list(map(lambda url: r'http://liuyan.people.com.cn' + url, UrlList))
        
        self.cityNums = len(forumUrlList)
        for url in forumUrlList:
            yield scrapy.Request(url=url,callback=self.getCityFid)

    def getCityFid(self, response):
        # Links of city and district leaders' comment
        leaderUrlList = response.xpath('//a[@class="message_index"]/@href').getall() + response.xpath('//a[@class="count-limit"]/@href').getall()
        for leaderUrl in leaderUrlList:
            self.fidList.append(leaderUrl.split('=')[-1])
        
        self.cityNums -= 1
        if self.cityNums < 1:
            for fid in self.fidList:
                print("Get `tid` from `fid` = %s" % fid)
                tids = []
                try:
                    tids = getTid(int(fid), self.domainName)
                except:
                    print("%s 获取失败" % fid)
                url = 'http://liuyan.people.com.cn/threads/content?tid='
                for tid in tids:
                    yield scrapy.Request(url=url + tid, callback=self.parse)

    def parse(self, response):
        # zone, name, title, status, tag, ctype, content, postTime, reply, replyTime
        
        item = CommentsItem()
        item['zone'] = response.xpath('//div[@class="path_2j w1200 grey2"]/a/text()')[-1].get()
        item['name'] = response.xpath('//div[@class="path_2j w1200 grey2"]/i/text()')[0].get()
        item['title'] = response.xpath('//span[@class="context-title-text"]/text()')[0].get()
        item['status'] = response.xpath('//div[@class="liuyan_box03 w1200 clearfix"]/h2/b/em/text()')[0].get()
        item['tag'] = response.xpath('//div[@class="liuyan_box03 w1200 clearfix"]/h2/b/em/text()')[1].get()
        item['ctype'] = response.xpath('//div[@class="liuyan_box03 w1200 clearfix"]/h2/b/em/text()')[2].get()
        item['content'] = ''.join(response.xpath('//p[@class="zoom content"]/text()').getall())
        time = response.xpath('//h3[@class="fl grey2 clearfix"]/span/text()')[0].get()
        item['postTime'] = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}', time).group()
        if response.xpath('//li[@class="reply"]'):
            item['reply'] = ''.join(response.xpath('//li[@class="reply"]/p[@class="zoom"]/text()').getall())
            time = response.xpath('//li[@class="reply"]/h3/em/text()')[0].get()
            item['replyTime'] = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}', time).group()
        else:
            item['reply'] = 'NULL'
            item['replyTime'] = 'NULL'

        yield item