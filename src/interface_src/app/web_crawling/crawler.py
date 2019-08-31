from lxml import etree
import pandas as pd
import datetime


xml1 = "Technology.xml"
xml2 = "Europe.xml"

def loadXML(url):     
    # creating tree element from given url 
    try:            
        tree = etree.parse(url)
        return tree
    except Exception as e:            
        print("An exception occurred in loadXML") 
        print( str(e))

def xpath(tree, path):
        # creating tree element from given url 
        try:            
            nodes = tree.xpath(path)
            return nodes
        except Exception as e:            
            print("An exception occurred in xpath") 
            print( str(e))

class NytimesCrawler:
    xml_path = ''
    tree = None
    title = ''           
    def __init__(self, xml_path):
        if xml_path:
            self.xml_path = xml_path
            self.tree = loadXML(xml_path)
            
    def crawlData(self):
        """funtion to crawl data according to the nytime xml design    
        Returns:
            df : dataframe of newsfeed
        """
        df = pd.DataFrame()   
        lst = []  
        if self.tree:
            category = xpath(self.tree, 'channel/title')
            items = xpath(self.tree, 'channel/item')
            media_ns = 'http://search.yahoo.com/mrss/'
            dc_ns = "http://purl.org/dc/elements/1.1/"
            if len(items) > 0:
                for item in items:
                    category = '; '.join(xpath(item, 'category/text()'))
                    creator = ''.join(xpath(item, "*[local-name() ='creator' and namespace-uri()='" + dc_ns + "']/text()"))
                    description = ''.join(xpath(item, 'description/text()'))
                    link = ''.join(xpath(item, 'link/text()'))
                    media_credit = ''.join(xpath(item, "*[local-name() ='credit' and namespace-uri()='" + media_ns + "']/text()"))
                    media_description = ''.join(xpath(item, "*[local-name() ='description' and namespace-uri()='" + media_ns + "']/text()"))
                    media_url = ''.join(xpath(item, "*[local-name() ='content' and namespace-uri()='" + media_ns + "']/@url"))
                    pubDate = ''.join(xpath(item, 'pubDate/text()'))
                    pubDate = datetime.datetime.strptime(pubDate[5:-6], '%d %b %Y %H:%M:%S')
                    title = ''.join(xpath(item, 'title/text()'))
                    lst.append([category, creator, description, link, media_credit, media_description, media_url, pubDate, title])                    
        df = pd.DataFrame(lst, columns = ["category", "creator", "description", "link", 'media_credit', "media_description", \
                                          "media_url", "pubDate", "title"])
        return df   
    

