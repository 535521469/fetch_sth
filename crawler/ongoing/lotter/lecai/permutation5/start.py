# encoding=utf8
'''
Created on 2013-3-22
@author: corleone
'''
from scrapy.cmdline import execute
from scrapy.settings import CrawlerSettings

if __name__ == '__main__':


    execute(argv=["scrapy", "crawl", "Permutation5Spider" ], settings=CrawlerSettings(__import__('crawler.ongoing.lotter.lecai.permutation5.settings', {}, {}, [''])))
#    execute(argv=["scrapy", "shell", "http://www.lecai.com/lottery/draw/list/4" ])

    


