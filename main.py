# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 09:20:32 2019

@author: Paola
"""

#------------------------------------------------------------------------------
#              SCRAPING DATA FROM WEB --- PAOLA ZOLA
#-----------------------------------------------------------------------------
import os
os.chdir(r'C:\Users\Paola\Dropbox\Web Scraping\python')
import pandas as pd
from StreamingData import Yahoo_realTime
from textMining1 import wikipedia_scrap
from solution import cds_scrap
from textMining2 import amazon_scraper
from textMining2 import trip_review_scraper
from textMining3 import FB_scraper
import datetime
import pickle
import json

#------------------------------------------------------------------------------
#                         Yahoo real time data
#----------------------------------------------------------------------------
#stock we want to scrap:
ticker='ENI.MI'
#when we want to finish:
finish_time = datetime.datetime.now() + datetime.timedelta(hours=0.3)
#time sleep (minuts) between the price queries:
delta=1

stocks_quote=Yahoo_realTime(ticker,finish_time,delta)
stocks_quote.to_csv('files/StreamingData.csv')


#-----------------------------------------------------------------------------
# rtstock pacakage (https://pypi.org/project/realtime-stock/)
from rtstock.stock import Stock
stock = Stock('AAPL')
stock.get_latest_price()


#-----------------------------------------------------------------------------
#                            wikipedia
#-----------------------------------------------------------------------------
wiki_url='https://it.wikipedia.org/wiki/Lisbona'
wikipedia_text=' '.join(wikipedia_scrap(wiki_url))
text_file = open("files/Wikipedia.txt", "w",encoding='utf-8')
text_file.write(wikipedia_text)
text_file.close()

#WIKIPEDIA API:
import wikipedia
print(wikipedia.WikipediaPage(title = 'Lisbon').summary)

wikipedia.set_lang("it")
wikipedia.summary("Facebook", sentences=1)



#-----------------------------------------------------------------------------
#               exercise: Scrape online news
#------------------------------------------------------------------------------
news_url='https://www.corriere.it/cronache/19_aprile_11/sestri-levante-urto-tir-bisarca-sull-a12-due-morti-33cd1b24-5c5f-11e9-b6d2-280acebb4d6e.shtml'
news=cds_scrap(news_url)




#-----------------------------------------------------------------------------
#                           tripadvisor
#----------------------------------------------------------------------------
url_tripadvisor='https://www.tripadvisor.it/Restaurant_Review-g187890-d9609651-Reviews-Bar_Giuffre-Palermo_Province_of_Palermo_Sicily.html'
tripadvisor_review,review_json=trip_review_scraper(url_tripadvisor)
folder='files'
tripadvisor_review_df=pd.concat(tripadvisor_review)
tripadvisor_review_df.to_csv(folder+'/tripadvisor_reviw.csv')
with open(folder+'/tripadisor_reviews.json', 'w') as outfile:
    json.dump(review_json, outfile)




#------------------------------------------------------------------------------
#                              amazon
#------------------------------------------------------------------------------
amazon_asin='B000WUFVR0' #yankee candle (ENG)
amazon_asin='B07GX4HHMP' #super mario

product_review=amazon_scraper(amazon_asin)
#save
with open('files/AmazonReview_yankeeCandle.pkl', 'wb') as f:
     pickle.dump(product_review, f)

#python module to scrape
from amazon_review_scraper import amazon_review_scraper
url = ("https://www.amazon.it/dp/B07H3CV89C/ref=gw_it_desk_h1_aucc_Ld_shlv_alx?pf_rd_p=e4a90667-fdd5-4993-bd27-f4e9688eafb2&pf_rd_r=YR0E0J8A3B505FVY3RVH")
start_page = 1
end_page = 1000
time_upper_limit = 1.4
file_name = "iphone6"

scraper = amazon_review_scraper.amazon_review_scraper(url, start_page, end_page, time_upper_limit)
scraper.scrape()
scraper.write_csv(file_name)
#------------------------------------------------------------------------------
#                         Facebook
#------------------------------------------------------------------------------
from selenium import webdriver
base_url = "https://www.facebook.com/"
path_browser_driver=r'C:\Users\Paola\WebScraping\selenium\webdriver\firefox\geckodriver.exe'
driver = webdriver.Firefox(executable_path=path_browser_driver)
driver.get(base_url)


username = driver.find_element_by_id("email")
password = driver.find_element_by_id("pass")

username.send_keys("") 
password.send_keys("") #il_pinguino02

l=driver.find_elements_by_id("loginbutton")
l[0].click()

base_url='https://www.facebook.com/LagoDiGardaLombardia/?ref=br_rs'
FacebookPage=FB_scraper(base_url, path_browser_driver, driver,'LagoDiGarda')
FacebookPage.to_csv('Facebook_LagoDiGarda.csv')


