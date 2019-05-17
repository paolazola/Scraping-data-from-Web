#----------------------------------------------------------------------------------------
#                       SCRAPING DATA USING R - Paola Zola 
#-----------------------------------------------------------------------------------------

if (!require("devtools")) {install.packages("devtools"); require("devtools")}  
if (!require("tm")) {install.packages("tm"); require("tm")}  
if (!require("stringr")) {install.packages("stringr"); require("stringr")} 
if (!require("RCurl")) {install.packages("RCurl"); require("RCurl")} 
if (!require("XML")) {install.packages("XML"); require("XML")} 
if (!require("twitteR")) {install.packages("twitteR"); library("twitteR")}  


#-----------------------------------------------------------------------------------
#                                 DOWNLOAD PDF
#-----------------------------------------------------------------------------------

downloadPDF <- function(filename, url, folder, handle, savename) { 
    dir.create(folder, showWarnings = FALSE) 
    
    
    page   <- getURL(url) #connect to the specified URL 
    parsed <- htmlParse(page) #get the html content
    links  <- xpathSApply(parsed, path="//a", xmlGetAttr, "href") #extract all a tags containing href element
    inds   <- grep("*.pdf", links) #find among the links the ones being .pdf
    links  <- links[inds] 
  
    #scrape pdf and save it
    if (!file.exists(str_c(folder, "/", savename))) { 
       content <- getBinaryURL(links, curl = handle) 
       writeBin(content, str_c(folder, "/", savename)) 
       Sys.sleep(1) 
    } 
}
#example:
folder<-'scrape_docs'
url_pdf<-"http://www.anvur.it/archivio-documenti-ufficiali/area-13_riviste-classe_a/"
filename_pdf<-'Area-13_riviste-Classe_A.pdf' #instead of white space ''-> -

handle <- getCurlHandle(useragent = str_c(R.version$platform, R.version$version.string, sep=", ")) 
downloadPDF(filename_pdf,url_pdf,folder, handle, filename_pdf)


#------------------------------------------------------------------------------
#                                 DOWNLOAD TABLES
#-----------------------------------------------------------------------------
if (!require("rvest")) {install.packages("rvest"); require("rvest")} 

# scrap single table
url = 'https://it.finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI'
yahoo <- read_html("https://it.finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI")
tables<-html_table(html_nodes(yahoo, "table"))
table_price<-tables[[1]]

#scrap and save prices for a series of stocks and/or stock index
quotes<-c('FCA.MI','^N225','RIO')
for (i in 1:length(quotes)){
  url<-paste0('https://it.finance.yahoo.com/quote/',quotes[i],'/history?p=',quotes[i])
  yahoo <- read_html(url)
  table<-html_table(html_nodes(yahoo, "table")[[1]])
  write.csv(table, str_c(folder, "/", quotes[i], ".csv"))
}

#---------------------------------------------------------------------------

#--------------------------------------------------------------------------
#                    API (TWITTER) 
#--------------------------------------------------------------------------
consumer_key <- ''
consumer_secret <- ''
access_token <- ''
access_secret <-''
setup_twitter_oauth(consumer_key,consumer_secret,access_token,access_secret)



queries=c('brescia','brixiae','bs') #fix the keywords
lingue='it'#,"en") #fix the languages
inizio="2019-05-12" #fix the starting date
area='45.5257,10.2283,10km' #fix the area in which we are interested


#brecia città
tweet_brescia<-data.frame()
for (i in 1:length(queries)){
  searchResults <- searchTwitter(queries[i], n =10000, geocode=area,lang=lingue,since=inizio)# Gather Tweets 
  Sys.setlocale("LC_ALL",'Italian')
  tweetFrame <- twListToDF(searchResults)  # Convert to a nice dF
  
  #tweetFrame$text<-str_trim(tweetFrame$text)
  df<-as.data.frame(tweetFrame)
  tweet_brescia<-rbind(tweet_brescia,df)
  
}
write.csv(tweet_brescia,file=paste0(folder,"/brescia_citta.csv"))



