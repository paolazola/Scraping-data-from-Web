# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 16:30:40 2017

@author: Paola
"""

#==============================================================================
#                       STREAMING STOCK PRICES -- Paola Zola
#==============================================================================




def Yahoo_realTime(ticker,finish_time,delta):
    import datetime
    import time
    import pandas as pd
    import requests
    from lxml import html
    from random import uniform

    url  = 'https://it.finance.yahoo.com/quote/'+str(ticker)+'?p='+str(ticker)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    
    list_values=[]
    list_timeNow=[]
    list_timeYahoo=[]
    while datetime.datetime.now() < finish_time:
        page = requests.get(url,headers = headers)
        time.sleep(uniform(2,3))
        #page_response = page.text #in this case we can use either page.content and page.text
        parser = html.fromstring(page.content)
        #Value
        #//text: owervise it will give the HTML element, in this way we have the text.
        value=parser.xpath('//span[@class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"]//text()')[0]
        #time:
        yahooTime=parser.xpath('//span[@data-reactid="37"]//text()')[0]
        #save:
        list_values.append(value)
        list_timeNow.append(datetime.datetime.now())
        list_timeYahoo.append(yahooTime)
        time.sleep(delta*60)
    dataframe=pd.DataFrame({'scraperTime':list_timeNow,'quotes':list_values,
                            'YahooPriceTime':list_timeYahoo})
    return(dataframe)

