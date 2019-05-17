# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 12:33:25 2019

@author: Paola
"""

from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360,proxies ={'https': 'https://193.92.85.51:8080'})
pytrends.build_payload(['easter'], cat=0, timeframe='today 5-y', geo='', gprop='')

HistoricalData=pytrends.get_historical_interest(['easter'], 
                                          year_start=2018,
                                          month_start=3, day_start=1,
                                          year_end=2018,
                                          month_end=4, day_end=30)
countries=pytrends.interest_by_region(resolution='COUNTRY') #city, metropolitan area
topics=pytrends.related_topics()
queries=pytrends.related_queries()