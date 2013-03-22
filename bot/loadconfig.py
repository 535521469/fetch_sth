# encoding=utf8
'''
Created on 2013-3-20
@author: corleone
'''

from bot.vo import DataSource, Provider, ProviderFetchCfg
from multiprocessing import Process
from sched import scheduler
from scrapy.cmdline import execute
from scrapy.settings import CrawlerSettings
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import aliased, sessionmaker
from zw.share.configutil import ConfigFile
import datetime
import os
import time

cfg_name = 'fetch.cfg'
cfg_path = os.path.join(os.path.pardir, cfg_name)
cfg = ConfigFile.readconfig(cfg_path)

mysql_engine = create_engine(('mysql://{user}:{passwd}@{host}:{port}/{db}'
                              u'?charset=utf8').format(**cfg.data[u'db'])
                             , encoding="utf-8", echo=0)

Session = sessionmaker(bind=mysql_engine)
session = Session()

class SpiderProcess(Process):
    
    def __init__(self, name, dp):
        Process.__init__(self)
        
        self.name = name
        self.dp = dp
        
    def run(self):
#        execute(argv, settings)
#        print self.dp.recordid
        settings = CrawlerSettings(__import__('crawler.ongoing.lotter.lecai.permutation5.settings', {}, {}, ['']))
        execute(argv=["scrapy", "crawl", self.dp.dfcfg.spidername ], settings=settings)
#        print u'in run '

def get_provider_config():
    alias_dp = aliased(Provider)
    alias_dpcfg = aliased(ProviderFetchCfg)
    
    dp_dfcfgs = session.query(alias_dp, alias_dpcfg)\
                .join(alias_dpcfg, ProviderFetchCfg)\
                .filter(alias_dp.enableflag == 1)\
                .filter(alias_dpcfg.enableflag == 1)
                
    for dp , dfcfg in dp_dfcfgs:
        dp.dfcfg = dfcfg
    
    dpid_dp = {}
    for dp in [dp for dp, dfcfg in dp_dfcfgs]:
        assert dp.recordid not in dpid_dp , (u"provider config "
                                    u"{dp.recordid} is duplucate").format(dp=dp)
        dpid_dp[dp.recordid] = dp
    return dpid_dp.values()

dps = get_provider_config()

def test(dp):
    print u' n test '
    sp = SpiderProcess(dp.recordid, dp)
    sp.run()


def add_task(root_scheduler, providers, max=3):
    
    print datetime.datetime.now()
    
    def check(unit_value, unit_exp, unit):
        locals()[unit] = unit_value
        if unit_exp == u"*":
            return 1
        else:
            return eval(unit_exp.format(**locals()))
    
    for i in range(max):
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
                
                root_scheduler.enterabs(time.mktime(target_time.timetuple()), 1, test, (dp,))
#    else:
#        root_scheduler.enter(max * 60, 0, add_task, (root_scheduler, providers, max))
                    
root_scheduler = scheduler(time.time, time.sleep)

root_scheduler.enter(0, 0, add_task, (root_scheduler, dps))
root_scheduler.run()



#add_task(root_scheduler, dps)
