# encoding=utf8
'''
Created on 2013-3-20
@author: corleone
'''
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Doc(Base):
    __tablename__ = u"DC_Doc"
    
    recordid = Column(u'RecordID', String(32), primary_key=True)
    docid = Column(u'DocID', String(32))
    filename = Column(u'FileName', String(256))
    filepath = Column(u'FilePath', String(256))
    filetype = Column(u'FileType', String(16))
    filesize = Column(u'FileSize', Integer)
    uploadtime = Column(u'UploadTime', DateTime)
    declaretime = Column(u'DeclareTime', DateTime)
    doctitle = Column(u'DocTitle', String(256))
    md5code = Column(u'MD5Code', String(128))
    statuscode = Column(u'StatusCode', Integer)
    providerid = Column(u'ProviderID', String(32))
    externalid = Column(u'ExternalID', String(512))
    mtime = Column(u'MTime', DateTime)
    ctime = Column(u'CTime', DateTime)
    
class DataSource(Base):
    __tablename__ = u"DC_DataSource"
    
    recordid = Column(u'RecordID', String(32), primary_key=True)
    sourcelabel = Column(u"SourceLabel", String(32))
    homepage = Column(u"HomePage", String(256))
    memo = Column(u"Memo", String)
    mtime = Column(u'MTime', DateTime)
    ctime = Column(u'CTime', DateTime)
    
    providers = relationship(u"Provider", backref=u"DC_DataSource")
    
class Provider(Base):
    
    def __init__(self, *args, **kws):
        self.dfcfg = None
    
    __tablename__ = u"DC_Provider"
    
    recordid = Column(u'RecordID', String(32), primary_key=True)
    url = Column(u"URL", String)
    label = Column(u"Label", String(128))
    datasourceid = Column(u"DataSourceID", String(32), ForeignKey('DC_DataSource.RecordID'))
    enableflag = Column(u"EnableFlag", Integer)
    memo = Column(u"Memo", String)
    startdate = Column(u"StartDate", DateTime)
    enddate = Column(u"EndDate", DateTime)
    mtime = Column(u'MTime', DateTime)
    ctime = Column(u'CTime', DateTime)
    
    providerfetchcfg = relationship(u'ProviderFetchCfg', backref=u"DC_Provider")
    
    
class ProviderFetchCfg(Base):
    __tablename__ = u"DC_ProviderFetchCfg"
    
    recordid = Column(u'RecordID', String(32), primary_key=True)
    spidername = Column(u"SpiderName", String(128))
    settingspath = Column(u"SettingsPath", String(256))
    minute = Column(u"Minute", String)
    hour = Column(u"Hour", String(128))
    dayofmonth = Column(u"DayOfMonth", String(32))
    month = Column(u"Month", Integer)
    weekday = Column(u"Weekday", Integer)
    enableflag = Column(u"EnableFlag", Integer)
    startdate = Column(u"StartDate", DateTime)
    enddate = Column(u"EndDate", DateTime)
    providerid = Column(u"ProviderID", String(32), ForeignKey(u'DC_Provider.RecordID'))
    memo = Column(u"Memo", String)
    mtime = Column(u'MTime', DateTime)
    ctime = Column(u'CTime', DateTime)

