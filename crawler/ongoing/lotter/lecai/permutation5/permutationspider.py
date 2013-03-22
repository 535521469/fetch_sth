'''
Created on 2013-3-20
@author: corleone
'''
from crawler.ongoing.lotter.lecai.spider import LeCaiHomeSpider
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector

class Permutation5Spider(LeCaiHomeSpider):
    
    url_part = u"/lottery/draw/list/4?lottery_type=4&ds=1900-01-01"
    
    name = u"Permutation5Spider"
    
    def start_requests(self):
        yield Request(self.home_url + self.url_part, self.parse)
        
    def parse(self, response):
        
        hxs = HtmlXPathSelector(response)
#        select('//table[@id="draw_list"]//tr')
        next_a_tag = hxs.select('//div[@class="page"]//a[@class="next"]')
        print response.url
        yield Request(next_a_tag.select('@href').extract()[0], self.parse)
    

