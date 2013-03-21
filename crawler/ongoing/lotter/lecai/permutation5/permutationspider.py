'''
Created on 2013-3-20
@author: corleone
'''
from crawler.ongoing.lotter.lecai.spider import LeCaiHomeSpider
from scrapy.http.request import Request

class Permutation5Spider(LeCaiHomeSpider):
    
    url_part = u"/lottery/draw/list/4"
    
    name = u"Permutation5Spider"
    
    def start_requests(self):
        yield Request(self.home_url + self.url_part, self.parse)
        
    def parse(self, response):
        
        with open(r'd:\fetch2.html', 'w') as f:
            f.write(response.body)
    
    
    
