# encoding=utf8
'''
Created on 2013-3-20
@author: corleone
'''
from sqlalchemy import Column, String, Table, MetaData, Integer, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
import sqlalchemy.types as types
from sqlalchemy.databases import mysql

from sqlalchemy.orm import sessionmaker
mysql_engine = create_engine('mysql://datatec:0.618@localhost:3306/DC?charset=utf8', encoding="utf-8", echo=True)

mysql_engine.execute("create database t2") #create db


