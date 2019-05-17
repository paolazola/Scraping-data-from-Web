# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 17:41:15 2019

@author: Paola
"""



#------------------------------------------------------------------------------
#                     WEB SCRAPING - PAOLA ZOLA-
#------------------------------------------------------------------------------


#==============================================================================
#                             TEXT MINING I
#==============================================================================

##scraper Wikipedia
def wikipedia_scrap(url):
    import urllib 
    import time
    from random import uniform
    from bs4 import BeautifulSoup
       
    page = urllib.request.urlopen(url)
    time.sleep(uniform(5,7))
    soup = BeautifulSoup(page, 'html.parser')
    
    #tabella=soup.find('table',{'class':'sinottico'}).text     
    ps=soup.findAll('p')
    testo=[]
    for t in range(0,len(ps)):
        testo.append(BeautifulSoup(ps[t].text, "lxml").text)
    
    #BeautifulSoup(ps[t].text, "lxml").text: ripulisce testo da html tags    
    return(testo)
    
        
