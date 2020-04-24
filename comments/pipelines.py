# -*- coding: utf-8 -*-
from openpyxl import Workbook

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CommentsPipeline(object):
    # zone, name, title, status tag, ctype, content, postTime, reply, replyTime
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['地区', '领导', '标题', '状态', '标签', '类型', '内容', '发布时间', '回复内容', '回复时间'])

    def process_item(self, item, spider):
        line = [item['zone'], item['name'], item['title'], item['status'], item['tag'], item['ctype'], item['content'], item['postTime'], item['reply'], item['replyTime']]
        self.ws.append(line)
        self.wb.save('comments.xlsx')
        return item
