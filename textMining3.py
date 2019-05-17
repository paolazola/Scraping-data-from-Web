# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:45:27 2018

@author: Utente
"""

def FB_scraper(base_url, path_browser_driver, driver,name):
    import time
    import pandas as pd
    from selenium import webdriver
    driver.get(base_url)
    name=name
    #--------------------------------------------------------------------------------
    #                                INFINITE SCROLLING:
    #--------------------------------------------------------------------------------
    pause = 5
    
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    print (lastHeight)
    zeta = 0
    
    #infinite scrolling:
    #driver.get_screenshot_as_file("test03_1_"+str(i)+".jpg")
   # while True:
   # scroll 5 times:
    for p in range(0,5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        for i in driver.find_elements_by_class_name("UFIPagerLink"):
            try:
                i.click()
                print(i)
            except Exception:
                print('yea')
        for j in driver.find_elements_by_class_name("see_more_link"):
             try:
                j.click()
                print(j)
             except Exception:
                print('yea')
        newHeight = driver.execute_script("return document.body.scrollHeight")
        print(newHeight)
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
        zeta +=1


    posts = driver.find_elements_by_xpath("//div[@class='_4-u2 _4-u8']")
    
    id_post=[]
    times=[]
    contenuto=[]
    condivisioni=[]
    likes=[]
    nr_comments=[]
    n=0
    for p in range(0,len(posts)):
        #ora e giorno
        try:
            data=posts[p].find_element_by_css_selector("abbr._5ptz").get_attribute("title")
            times.append(data)
            id_post.append(p)
        except:
            print('recensioni a fianco')
            n+=1
        
        #posts text:
        try:
            contenuti=posts[p].find_element_by_css_selector('div._5pbx.userContent._3576').text
            contenuto.append(contenuti)
            
        except:
            contenuto.append('none')
            
                
        #shares nr:
        try:
            share= posts[p].find_elements_by_css_selector("a._3rwx._42ft")
            condivisioni.append(share[0].text)
        except IndexError:
            condivisioni.append('none')
        #likes nr:
        try:
            like= posts[p].find_elements_by_css_selector("a._3dlf")
            likes.append(like[0].text.split('\n')[0])
        except IndexError:
            likes.append('none')
        #comments number:
        try:
            nrComm= posts[p].find_elements_by_css_selector("a._3hg-._42ft")
            nr_comments.append(nrComm[0].text)
        except IndexError:
            nr_comments.append('none')
            
            
    #clean for the case of advertise posts:       
    if len(times)!=len(contenuto) and len(times)!=len(condivisioni):
        diff=len(contenuto)-len(times)
        contenuto=contenuto[diff:]
        condivisioni=condivisioni[diff:]
        posts=posts[diff:]
        likes=likes[diff:]
        nr_comments=nr_comments[diff:]
        

    fb_page=pd.DataFrame({'utente':name,'data':times,'post':contenuto,'id post':id_post,'likes':likes, 'share': condivisioni,'comments number':nr_comments})
 
    return(fb_page)


    
