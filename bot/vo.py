# encoding=utf8
'''
Created on 2013-3-20
@author: corleone
'''
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import aliased, sessionmaker, relationship

mysql_engine = create_engine('mysql://datatec:0.618@localhost:3306/DC?charset=utf8', encoding="utf-8", echo=True)
Session = sessionmaker(bind=mysql_engine)
Base = declarative_base()
session = Session()

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


class ProviderFetchCfg(Base):
    __tablename__ = u"DC_ProviderFetchCfg"
    
    recordid = Column(u'RecordID', String(32), primary_key=True)
    minute = Column(u"Minute", String)
    hour = Column(u"Hour", String(128))
    dayofmonth = Column(u"DayOfMonth", String(32))
    month = Column(u"Month", Integer)
    weekday = Column(u"Weekday", Integer)
    enableflag = Column(u"EnableFlag", Integer)
    startdate = Column(u"StartDate", DateTime)
    enddate = Column(u"EndDate", DateTime)
    providerid = Column(u"ProviderID", String(32))
    memo = Column(u"Memo", String)
    mtime = Column(u'MTime', DateTime)
    ctime = Column(u'CTime', DateTime)

#alias_ds = aliased(DataSource)
#alias_dp = aliased(Provider)

#for p, pc in session.query(DataSource, Provider).filter(DataSource.recordid == Provider.datasourceid)\
#                       .filter(Provider.enableflag == 1):
#    print p.recordid, pc.recordid

for ds in session.query(DataSource):
    print ds.providers



