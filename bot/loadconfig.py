# encoding=utf8
'''
Created on 2013-3-20
@author: corleone
'''

from zw.share.configutil import ConfigFile
import os

cfg_name = 'fetch.cfg'

cfg_path = os.path.join(os.path.pardir, cfg_name)

cfg = ConfigFile.readconfig(cfg_path)



