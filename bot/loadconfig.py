# encoding=utf8
'''
Created on 2013-3-20
@author: corleone
'''

from bot.vo import Provider, ProviderFetchCfg
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import aliased, sessionmaker
from zw.share.configutil import ConfigFile
import os

cfg_name = 'fetch.cfg'
cfg_path = os.path.join(os.path.pardir, cfg_name)
cfg = ConfigFile.readconfig(cfg_path)

mysql_engine = create_engine(('mysql://{user}:{passwd}@{host}:{port}/{db}'
                              u'?charset=utf8').format(**cfg.data[u'db'])
                             , encoding="utf-8", echo=0)

Session = sessionmaker(bind=mysql_engine)
session = Session()

def get_provider_config():
    alias_dp = aliased(Provider)
    alias_dpcfg = aliased(ProviderFetchCfg)
    
    dp_dfcfgs = session.query(alias_dp, alias_dpcfg)\
                .join(alias_dpcfg, ProviderFetchCfg)\
                .filter(alias_dp.enableflag == 1)\
                .filter(alias_dpcfg.enableflag == 1).all()
                
    for dp , dfcfg in dp_dfcfgs:
        dp.dfcfg = dfcfg
    
    dpid_dp = {}
    for dp in [dp for dp, dfcfg in dp_dfcfgs]:
        assert dp.recordid not in dpid_dp , (u"provider config "
                                    u"{dp.recordid} is duplucate").format(dp=dp)
        dpid_dp[dp.recordid] = dp
    
    
    
    return dpid_dp.values()





#add_task(root_scheduler, dps)
