# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 09:29:16 2019

@author: Paola
"""

#-----------------------------------------------------------------------------
#                 scrape news from online journals
#-----------------------------------------------------------------------------

#=============================================================================
#                 CORRIERE DELLA SERA --- esercizio---
#=============================================================================

url='https://www.corriere.it/cronache/19_aprile_11/sestri-levante-urto-tir-bisarca-sull-a12-due-morti-33cd1b24-5c5f-11e9-b6d2-280acebb4d6e.shtml'
def cds_scrap(url):
    import urllib 
    import time
    from random import uniform
    from bs4 import BeautifulSoup
       
    page = urllib.request.urlopen(url)
    time.sleep(uniform(5,7))
    soup = BeautifulSoup(page, 'html.parser')
    
    title=soup.find('h1',{'class':'article-title'}).text
    
    subtitles=soup.find('h2',{'class':'article-subtitle'}).text
    
    contenuto=soup.find('p',{'class':'chapter-paragraph'}).text
    return(title, subtitles, contenuto)
    

