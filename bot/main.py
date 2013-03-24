# encoding=utf8
'''
Created on 2013-3-20
@author: corleone
'''
from bot.loadconfig import get_provider_config
from multiprocessing import Process
from sched import scheduler
from scrapy.settings import CrawlerSettings
import datetime
import multiprocessing
import time
from scrapy.cmdline import execute

class SpiderProcess(Process):
    
    def __init__(self, dp):
        Process.__init__(self)
        self.dp = dp
        self.name = dp.dfcfg.spidername
        
        
    def run(self):

        try:
            settings = CrawlerSettings(__import__(self.dp.dfcfg.settingspath, {}, {}, ['']))
            execute(argv=["scrapy", "crawl", self.dp.dfcfg.spidername ], settings=settings)
        except Exception as e:
            raise e

spider_process_mapping = {}

def add_task(root_scheduler, providers, minute_range=1):
    
    def check(unit_value, unit_exp, unit):
        locals()[unit] = unit_value
        if unit_exp == u"*":
            return 1
        else:
            return eval(unit_exp.format(**locals()))
    
    for i in range(minute_range):
        target_time = datetime.datetime.now() + datetime.timedelta(minutes=i)
        for dp in providers:
            if all(map(lambda x:check(*x), ((target_time.minute, dp.dfcfg.minute, 'minute')\
                              , (target_time.hour, dp.dfcfg.hour, 'hour')
                              , (target_time.day, dp.dfcfg.dayofmonth, 'dayofmonth')
                              , (target_time.date, dp.dfcfg.weekday, 'weekday')
                              , (target_time.month, dp.dfcfg.month, 'month')
                              ))):
                
                timetuple = list(target_time.timetuple()[:5]) + [0, ]
                target_time = datetime.datetime(*timetuple)
                p = spider_process_mapping.get(dp.dfcfg.spidername)
                if p:
                    if p.is_alive():
                        print p.is_alive(), dp.dfcfg.spidername
                        break
                    
                p = SpiderProcess(dp)
                spider_process_mapping[dp.dfcfg.spidername] = p
                root_scheduler.enterabs(time.mktime(target_time.timetuple()), 1, p.start, ())
                    
    else:
        root_scheduler.enter(minute_range * 60, 0, add_task, (root_scheduler, providers, minute_range))
         

if __name__ == '__main__':
    dps = get_provider_config()
    
    
    multiprocessing.freeze_support()
    root_scheduler = scheduler(time.time, time.sleep)
    root_scheduler.enter(0, 0, add_task, (root_scheduler, dps))
    root_scheduler.run()

