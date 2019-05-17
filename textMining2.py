# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 13:26:52 2018

@author: Paola Zola
"""
#==============================================================================
#              TEXT MINING II: AMAZON AND TRIPADVISOR --PAOLA ZOLA--
#==============================================================================

#=============================================================================
#                              AMAZON
#==============================================================================
def amazon_scraper(asin):
       import requests
       from lxml import html
       import time
       from random import uniform
       import progressbar
       def find_between( s, first, last ):
            try:
                start = s.index( first ) + len( first )
                end = s.index( last, start )
                return s[start:end]
            except ValueError:
                return ""

       valid= False
       while not valid:  
               amazon_url  = 'http://www.amazon.com/dp/'+asin
               headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
               #headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'}
               page = requests.get(amazon_url,headers = headers)
               time.sleep(uniform(3,5))
               page_response = page.content
               time.sleep(uniform(3,4))
               parser = html.fromstring(page_response)
               reviews_number=' '.join(parser.xpath('//span[@id="acrCustomerReviewText"]//text()')).split(' ')[0] 
               reviews_number=reviews_number.replace(',','')
               if len( reviews_number)!=0:
                  valid=True
       valid2=False
       while not valid2:
           try:
               amazon_url  = 'http://www.amazon.com/dp/'+asin
               headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
               #headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'}
               page = requests.get(amazon_url,headers = headers)
               time.sleep(uniform(3,5))
               page_response = page.content
               time.sleep(uniform(3,4))
               parser = html.fromstring(page_response)
                 
               #get the numebr of reviews:
               #get the link to the reviews page:
               elt=parser.xpath('//a[@id="dp-summary-see-all-reviews"]')
               link=elt[0].attrib['href']
               valid2=True
           except IndexError:
               print('try again')
       
       
       url='http://www.amazon.com'+link
       
       #now we need to slightly modify the url in order to query to different pages:
       urlOK=url.replace('ref=cm_cr_dp_d_show_all_top?ie=UTF8&reviewerType=all_reviews',
                   'ref=cm_cr_arp_d_paging_btm_next_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1')
       
       #find the piece of url to substiture with the page number
       #changeFIRST=find_between(urlOK, 'next_', '?') 
       #changeSECOND=urlOK.split('=')[-1]
       product_reviews={}
       list_page_rec=[]
       
       bar=progressbar.ProgressBar()
       for i in bar(range(1,int(int(reviews_number)/9))):
           valid3=False
           while not valid3: 
               url1=urlOK.replace(urlOK.split('=')[-1],str(i)) #to substitute the page to load  
               headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'}       
               #headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
                  
               page=requests.get(url1,headers = headers)
               time.sleep(uniform(3,6))
               page_response= page.content
               parser = html.fromstring(page_response)
               
               reviews=parser.xpath('//div[@data-hook="review"]')
               if len(reviews)!=0:
                   valid3=True
           id=[]
           for review in reviews:
              id.append(review.attrib['id'])
           
           rec=[]
           for item in id:
               rec.append(parser.xpath('//div[@id="'+str(item)+'"]//text()'))
           
           #we have all the item of the review. Lets create a dict for each user
           #lets create a dict for every review with authors, date, rating, title and content:
           
           for review in rec:
               dict_Rec=dict.fromkeys(['author','date','rating','title','text'])
               data=review
               #clean from html go head tag
               data = [item for item in data if not str(item).startswith('\n')]
              
               dict_Rec['author']=str(data[0])
               dict_Rec['rating']=str(data[1])
               dict_Rec['title']=str(data[2])
               dict_Rec['date']=str(data[3])
               dict_Rec['text']=str(data[6:len(data)])
               list_page_rec.append(dict_Rec)
           
       for d in range(0,len(list_page_rec)):
          product_reviews[d]=list_page_rec[d]
       
       return(product_reviews)
        
#==============================================================================
#                            TRIPADVISOR
#==============================================================================

def trip_review_scraper(url_originale):
    import urllib 
    import progressbar
    import json
    import time
    from random import uniform
    from bs4 import BeautifulSoup
    import pandas as pd
    import math

#    import re
    def find_between( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""
    index_pages_0 = url_originale
    
    page = urllib.request.urlopen(index_pages_0) #create the request to the server
    time.sleep(uniform(2,3)) #give the time to load the page
    soup = BeautifulSoup(page, 'html.parser') #extract the html text from the page
    
    #lets identify the number of total pages:
    v=soup.find_all('div',{"class": "pagination-details"})
    n_rec=[int(s) for s in (v[0].text).split() if s.isdigit()][2]
    num_pages=math.floor(n_rec/10) #each page has 10 reviews, so let's fix the number of iterations of the code
            
    #the link of each group of 10 reviews
    index_pages = []
    index_pages.append(index_pages_0)
    for i in range(1,int(num_pages)):
        pezzo=find_between(index_pages_0,'https','Reviews-')
        index_pages.append('https' + pezzo + 'Reviews-' +'or'+str(i*10) +'-' + index_pages_0.split('Reviews-',1)[1])      
    
    trip=[]
    trip_json=[]
    
    #now for each group of 10 reviews lets extract the link of the single review
    bar = progressbar.ProgressBar()
    for k in bar(range(0,len(index_pages))):
        page = urllib.request.urlopen(index_pages[k])
        time.sleep(uniform(2,4))
        soup = BeautifulSoup(page, 'html.parser') 
        
        #get the url in the pages and clean it keeping only the ones related to reviews
        link=[]
        for a in soup.find_all('a', href=True):
            link.append(a['href'])
        
        to_match=find_between( url_originale, 'Reviews-', '.html' )
        link_light=[f for f in link if to_match in f]
        link_2light=[f for f in link_light if 'ShowUserReviews' in f]
        
        titles=[]
        names=[]
        author_loc=[]
        date=[]
        contenuto=[]
        stars=[]
        
        for p in range(0,len(link_2light)):
            
            page = urllib.request.urlopen('https://www.tripadvisor.it/'+str(link_2light[p]))
            time.sleep(uniform(3,7))
            soup = BeautifulSoup(page, 'html.parser')
            
            #every review has a json format :) easy...
            script = soup.find('script', type='application/ld+json').text
            alfa= json.loads(str(script))
            trip_json.append(alfa)
              
            
            names.append(soup.find('span',{'class':'expand_inline scrname'}).text)  #author name
            author_loc.append(soup.find('span',{'class':'expand_inline userLocation'}).text) #author location
            
            date.append(soup.find('span',{"class": "ratingDate relativeDate"}).text) #review date

            contenuto.append(alfa['reviewBody']) #review body
            stars.append(int(alfa['reviewRating']['ratingValue'])) #rating
            titles.append(alfa['name']) #review title
            
        recensione=pd.DataFrame({'name':names,'author Location': author_loc, 'title':titles, 'date':date, 'rating':stars, 'text':contenuto})
        
        trip.append(recensione)
       # trip_json.append(alfa)
    return(trip,trip_json)