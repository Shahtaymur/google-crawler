import flask
import json
import requests
import urllib
from urllib.request import Request, urlopen
from urllib.parse import quote_plus, urlparse, parse_qs
from bs4 import BeautifulSoup
import time
#import urllib.request as urllib
from flask_restful import Resource, Api, reqparse
from flask import request
from random import choice

from requests.sessions import default_headers
import config
import logging
import random
import re
import os
from http.cookiejar import LWPCookieJar
import ssl
USE_PROXY = []

global logger
logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',datefmt='%d-%m-%Y:%H:%M:%S',level=logging.DEBUG,filename='app.log')
logger = logging.getLogger('g_crawler.py')

class GCrawler(Resource):

    # def __init__(self,query) -> None:
    #     self.query = query
    #     self.result = self.google_search(self.query)
       
    def get(self):
        q_string = request.args.get('q')
        add_faqs = request.args.get('faqs')
        r_cache = request.args.get('r_cache')
        if not q_string:
            return {'message': "invalid request pls add search para and try again.. e.g http://127.0.0.1:5000/search?q=apple"}, 405
        self.query = q_string
        self.add_faqs = add_faqs
        filename = re.sub('[^A-Za-z0-9]+', '', self.query)
        if not r_cache == 'yes':
            try:
                with open(f'cache/{filename}.json') as json_file:
                    self.result = json.load(json_file)
            except Exception as e:
                logger.info('>> no cache found {} now get result from google.'.format(str(e)))
                self.result =  self.google_search(self.query)
        else:
            self.result =  self.google_search(self.query)
        
        with open(f'cache/{filename}.json', 'w', encoding ='utf8') as json_file:
            json.dump(self.result, json_file, ensure_ascii = False)
        return {'data': self.result}, 200

    def get_source(self,url):
        """Return the source code for the provided URL. 

        Args: 
            url (string): URL of the page to scrape.

        Returns:
            response (object): HTTP response object from requests_html. 
        """
        try:
            time.sleep(random.randint(2,5))  # be nice with google :)
            print('>> trying to get result from "{}"'.format(url))
            count = 1
            req = None
            while True:
                #DEFAULT_HEADERS = {
                #  'authority': 'www.google.com',
                #'method': 'GET',
                #'accept-language': 'en-PK',
                #  'scheme': 'https',
                #  'accept': "*/*",
                #  'accept-encoding': 'gzip, deflate, br',
                 #'accept-language': 'en-US',
                #'user-agent':choice(config.USER_AGENTS)
                #}
                DEFAULT_HEADERS = {
                    'User-agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
                    'accept-language': 'en-US',
                    'scheme': 'https'
                }

                params = {
                    'q': url,
                    'gl': 'pk', # country where to search from
                    'hl': 'en',
                }
                DNS = choice(config.GEONODS)
                if len(config.GEONODS) == config.BLOCK_DNS:
                    return {'status':'failed','req':None}
                while DNS in USE_PROXY or DNS in config.BLOCK_DNS:
                    DNS = choice(config.GEONODS)
                    
                USE_PROXY.append(DNS)

                proxy = {"https":"http://{}:{}@{}".format(config.PROXY_USER, config.PROXY_PASS, DNS)}
                try:
                    
                    req = requests.get('https://www.google.com/search', proxies=proxy,headers=DEFAULT_HEADERS,params=params,timeout=60)
                    if req.status_code in [200, 404]:
                        print('>> request returned {} total request "{}"'.format(req.status_code,count))
                        break
                    elif req.status_code == 429:
                        self.add_block_dns(DNS)
                        logger.error(req.headers)

                    print('>> request returned {} total request "{}"'.format(req.status_code,count))
                except requests.exceptions.ConnectionError:
                    print('>> proxy not connect')
                except requests.exceptions.RequestException as e:
                    logger.error(e.request.headers)
                    logger.error(e.args[0].reason)
                    pass
                count = count + 1
            return {'status':'success','req':req}
        except requests.exceptions.RequestException as e:
            print(e)
            logger.error('error occured.{}'.format(str(e)))
            return {'status':'failed','req':req}

    def add_block_dns(self,dns):
        if len(config.GEONODS)-len(config.BLOCK_DNS) < 1000:
            self.reset_dns(dns)
        with open('block_dns.txt', 'a') as bd:
            if len(config.BLOCK_DNS)>0:
                bd.write(f'\n{dns}')
            else:
                bd.write(f'{dns}')
            logger.debug('blocked dns : "{}"'.format(dns))
        config.BLOCK_DNS.append(dns)

    def reset_dns(self,dns):
        open('block_dns.txt', mode='w').close()
        config.BLOCK_DNS = []

    def get_results(self,query):
        #create url
        query = urllib.parse.quote_plus(query)
        #response = self.get_source('https://www.google.co.uk/search?q='+query)
        response = self.get_source(query)
        print('>> request on google on "{}"'.format(query))
        return response
        
    def parse_results(self,response):
        print('>> trying to get meta description from google')
        soup = BeautifulSoup(response.text,"html.parser")
        
        #get meta description on web page
        results = soup.find_all('div','tF2Cxc')
        if len(results) == 0:
            soup = soup.find('body')
            results = soup.find_all('div','ezO2md')

        #check feature snippet on web page
        feature_snippet = soup.find('h2')
         
        output = []
        answer = []
        unit_converter = {}
        if feature_snippet:
            for snippet in feature_snippet:
                if snippet == "Featured snippet from the web":
                    #get feature snippet from page response
                    answer.append(self.get_answer(soup))
                    break
                elif snippet == "Unit converter":
                    #get unit converter from page response
                    print('>> crawl unit converter')
                    soup = BeautifulSoup(response.content,"html.parser")
                    card = soup.find('div',{'data-hveid':'CAIQAQ'})
                    unit_converter['type'] = []
                    if card:
                        try:
                            type = card.find('select',{'jsname':'MVliGc'})
                            for option in type.find_all('option'):
                                if 'selected' in option.attrs:
                                    unit_converter['type'].append({'value':option.text,'selected':True})
                                else:
                                    unit_converter['type'].append(option.text)
                            left = card.find('div',{'id':'HG5Seb'})
                            unit_converter['l_value'] = left.find('input').attrs['value']
                            unit_converter['l_type'] = []
                            for x in left.find_all('option'):
                                if 'selected' in x.attrs:
                                    unit_converter['l_type'].append({'value':x.text,'selected':True})
                                else:
                                    unit_converter['l_type'].append(x.text)
                            right = card.find('div',{'id':'NotFQb'})
                            unit_converter['r_value'] = right.find('input').attrs['value']
                            unit_converter['r_type'] = []
                            for x in right.find_all('option'):
                                if 'selected' in x.attrs:
                                    unit_converter['r_type'].append({'value':x.text,'selected':True})
                                else:
                                    unit_converter['r_type'].append(x.text)
                            unit_converter['formula'] = card.find('div',{'dtp2jf'}).find('table').text
                        except Exception as e:
                            logger.error('error occured.{}'.format(str(e)))
                            pass
                
        for i,result in enumerate(results):
            print('>> get meta description...')
            item = {}
            item['text'] = None
            item['text_prefix'] = None
            if result.find('h3') or result.find('div','Dks9wf'):
                try:
                    item['title'] = result.find('h3').text
                except:
                    item['title'] = result.find('a').find('span').text

                item['link'] = result.find('a').attrs['href']
                if i == 0 and len(answer) > 0 and not answer == '':
                    item['snippet'] = answer[0]
                else:
                    meta_description = result.find('div','IsZvec')
                    if meta_description is None:
                        meta_description = result.find('div','Dks9wf')
                    table  = meta_description.find('table')
                    if table:
                        try:
                            item['meta_data'] = self.get_table(table)
                        except Exception as e:
                            logger.error('error occured.{}'.format(str(e)))
                            pass

                    try:
                        item['text_prefix'] = meta_description.find('span',{'class':'MUxGbd wuQ4Ob WZ8Tjf'}).text
                    except Exception as e:
                        logger.debug('>> no key found{}'.format(str(e)))
                    
                    item['text'] = meta_description.text

                    try:
                        item['text'] = meta_description.find('div',{'class':'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf'}).text
                    except Exception as e:
                        logger.debug('>> text not found{}'.format(str(e)))

                    if not item['text_prefix'] is None:
                        item['text'] = item['text'].replace(item['text_prefix'],'').replace(' — ','')
                    
                    if item['text'] is None or item['text'] == "":
                        item['text'] = meta_description.text
                
                output.append(item)
        return {'output':output,'unit_converter':unit_converter}

    def get_answer(self,document,question=None):
        print('>> trying to scrape feature snipper from page response')
        fea_sni = document.find('div','V3FYCf')
        if not fea_sni:
            fea_sni = document.find('div',{'class':'V3FYCf'})
        data = {}
        if fea_sni:
            if not question == None:
                data = {'question':question}
            try:
                headings = fea_sni.find_all('div',{'role':'heading','aria-level':'3'})
                for i,heading in enumerate(headings):
                    data['heading' if i == 0 else 'heading{}'.format(i+1)] = heading.text
            except Exception as e:
                try:
                    headings = fea_sni.find('div',{'role':'heading','aria-level':'3'})
                    data['heading' if i == 0 else 'heading{}'.format(i+1)] = heading.text
                except Exception as e:
                    logger.error('>> not heading found in feature snippet')

            title = fea_sni.find('div','yuRUbf')
            if title:
                data['title'] = title.find('h3').text
                data['link'] = title.find('a').attrs['href']
            if fea_sni.find('ol'):
                data['snippet_data'] = self.get_list(fea_sni,'ol')
                data['snippet_type'] = 'Ordered Featured Snippet'
                print('>> ordered list found in feature snippet')
            elif fea_sni.find('ul'):
                data['snippet_data'] = self.get_list(fea_sni,'ul')
                data['snippet_type'] = 'Unordered Featured Snippet'
                print('>> unordered list found in feature snippet')
            elif fea_sni.find('table'):
                data['snippet_data'] = self.get_table(fea_sni)
                data['snippet_type'] = 'Table Featured Snippet'
                print('>> table found in feature snippet')
            else:
                try:
                    data['heading'] = fea_sni.find('span',{'class':'ILfuVd'}).text
                except Exception as e:
                    logger.error('>> not heading found in feature snippet "{}"'.format(str(e)))
                data['snippet_type'] = 'Definition Featured Snippet'
            try:
                data['date'] = (fea_sni.find('div','xzrguc') or fea_sni.find('span',{'class':'kX21rb ZYHQ7e'})).text
                data['heading'] = self.replace_last(data['heading'],data['date'],'')
            except Exception as e:
                logger.error('error occured.{}'.format(str(e)))
                pass

        return data

    def replace_last(self,source_string, replace_what, replace_with):
        head, _sep, tail = source_string.rpartition(replace_what)
        return head + replace_with + tail

    def get_list(self,document,type):
        ol = document.find(type)
        data = []
        try:
            list = ol.find_all('li')
            for li in list:
                data.append(li.text)
                #print(li.text)
        except Exception as e:
            logger.error('error occured.{}'.format(str(e)))
            pass
        return data

    def get_table(self,document):
        tr = document.find_all('tr')
        header = []
        values = []
        for row in tr:
            th = row.find_all('th')
            if th:
                for x in th:
                    header.append(x.text)
            else:
                td = row.find_all('td')
                value = []
                for x in td:
                    value.append(x.text)
                values.append(value)
        return {'columns':header,'values':values}

    def get_dictionary(self,response):
        soup = BeautifulSoup(response.text,"html.parser")
        #dictionary = soup.find("div", {"role": "heading", "aria-level": "2","class":"gJBeNe vbr5i"})
        dictionary = soup.find('div',{"class":"obcontainer"})
        dfn = {'dictionary':[]}
        if dictionary:
            try:
                dfn['word'] = dictionary.find('div',{"class":"jY7QFf"}).text
                #def_mod = dictionary.find('div',{"class":"vmod"})
                def_type = dictionary.find_all('div',{"jsname":"r5Nvmf",'class':'vmod'})
                for type in def_type:
                    dfnlist = {'def_list':[]}
                    dfnlist['type'] = type.find('div',{"jsname":"jUIvqc",'class':'xpdxpnd'}).text
                    def_mod = type.select("ol[class='eQJLDd']")
                    for mod in def_mod:
                        lis = mod.find_all('li',{"jsname":"gskXhf"})
                        for li in lis:
                            try:
                                item = {
                                    'definition': li.find('div',{'data-dobid':"dfn"}).text,
                                    'example': li.select("div[class='vmod']")[1].text,
                                    'similer':[]
                                }
                                simis = li.find_all('div',{"role":'listitem'})                            
                                for smi in simis:
                                    item['similer'].append(smi.text)
                                    print(smi.text)
                                dfnlist['def_list'].append(item)
                            except Exception as e:
                                logger.error('error occured.{}'.format(str(e)))
                                pass
                    dfn['dictionary'].append(dfnlist)
            except Exception as e:
                logger.error('error occured.{}'.format(str(e)))
                pass
        return dfn

    def get_popular_products(self,response):
        print('>> get popular product list...')
        soup = BeautifulSoup(response.text,"html.parser")
        cards = soup.find('g-scrolling-carousel')
        cards_list = {'popular_products':[]}
        if cards:
            cards = cards.find_all('div',{'class','WGwSK SoZvjb'})
            for card in cards:
                cards_list['popular_products'].append(card.text)
                
        return cards_list

    def get_top_sights(self,response):
        print('>> get top sights list...')
        soup = BeautifulSoup(response.text,"html.parser")
        topsight = soup.find('g-scrolling-carousel')
        top_list = {'data':[]}
        if topsight:
            if soup.find('g-tray-header'):
                top_list['title'] = soup.find('g-tray-header').text
                topsight = soup.find_all('div',{'class':'rqTuzc'})
                for list in topsight:
                    try:
                        item = {
                            'item': list.find('span','aVSTQd oz3cqf rOVRL').text,
                            'value': list.find('span','ZIF80').text,
                            'link':'https://www.google.com/{}'.format(list.find('a')['href'])
                        }
                        top_list['data'].append(item)
                    except Exception as e:
                        logger.error('error occured.{}'.format(str(e)))
                        pass

        return top_list

    def get_videos(self,response):
        print('>> get videos list...')
        soup = BeautifulSoup(response.text,"html.parser")
        videos = soup.find_all('div',{"jsname":"TFTr6"})
        video_list = {'data':[]}
        if videos:
            video_list['type'] = 'videos'
            for video in videos:
                try:
                    title = None
                    link = None
                    date = None
                    raw_data = None
                    try:
                        title = video.find('div','uOId3b').text
                        link = video.find('a')['href']
                        date = video.find('div','hMJ0yc').text
                        raw_data = video.find('a')['aria-label']
                    except Exception as e:
                        logger.error('error occured.{}'.format(str(e)))
                        pass
                    if not title == None:
                        item = {
                            'link' : link,
                            'title' : title,
                            'date' : date,
                            'raw_data' : raw_data
                        }
                        video_list['data'].append(item)
                except Exception as e:
                    logger.error('error occured.{}'.format(str(e)))
                    pass

        return video_list

    def get_oraganic(self,response):
        print('>> get organic list...')
        soup = BeautifulSoup(response.text,"html.parser")
        recipes = soup.find_all('g-link')
        recip_list = {'data':[]}
        if recipes:
            recip_list['type'] = 'organic'
            for recip in recipes:
                title = None
                name = None
                link = None
                duration = None
                description = None
                try:
                    try:
                        title = recip.find('div',{'aria-level':'3','role':'heading'}).text
                        name = recip.find('cite').text
                        link = 'https://www.google.com/{}'.format(recip.find('a')['href'])
                        duration = recip.find('div',{'class':'L5KuY Eq0J8'}).text
                        description = recip.find('div',{'class':'LDr9cf L5KuY'}).text
                    except Exception as e:
                        logger.error('error occured.{}'.format(str(e)))
                        pass
                    if not title == None:
                        item = {
                            'title': title,
                            'name': name,
                            'duration':duration,
                            'description':description,
                            'link':link
                        }
                        recip_list['data'].append(item)
                except Exception as e:
                    logger.error('error occured.{}'.format(str(e)))
                    pass

        return recip_list

    #people_alse_ask
    def extractQuestionData(self,document):
        data = []
        print('>> get related questions..')
        soup = BeautifulSoup(document.content,"html.parser")
        rel_questions = soup.find_all('div',{'class':'related-question-pair'})
        for question in rel_questions:
            title = question.find('div',{'jsname':'jIA8B'}).text
            time.sleep(random.randint(2,5)) #be nice with google
            req = self.get_results(title)
            if req['status'] == 'failed':
                continue
            response = req['req']
            try:
                with open(f"html/{re.sub('[^A-Za-z0-9]+', '', title)}.html", "w",encoding="utf-8") as file:
                    file.write(response.text)
            except Exception as e:
                print(e)
                pass
            soup = BeautifulSoup(response.content,"html.parser")
            
            results = soup.find_all('div','tF2Cxc')
            if len(results) == 0:
                soup = BeautifulSoup(response.text,"html.parser")
                soup = soup.find('body')
            answer = self.get_answer(soup,title)
            if answer:
                data.append(answer)
                print('>> get related answer of "{question}" - "{answer}"'.format(question=title,answer=answer['snippet_type']))
        return data

    def extract_information(self,soup : BeautifulSoup):
        print('>> get information from google...')
        information = {'attributes':[]}
        try:
            description = str(soup.select_one(".kno-rdesc").text)[11:]
            attributes = soup.find_all("div", {"class": "Z1hOCe"})
            #soup.find_elements_by_class_name("Z1hOCe")
            information['description'] = description.replace("\n","")
            for attribute in attributes:
                if(attribute.text):
                    info = attribute.text.split(":",1)
                    information['attributes'].append({'key':info[0].replace("\n",""),'value':info[1].replace("\n","")})
        except Exception as e:
            logger.error('error occured.{}'.format(str(e)))
            pass
        return information

    def get_rel_keywords(self,response):
        print('>> get related keyword...')
        soup = BeautifulSoup(response.text,"html.parser")
        keywords = []
        keys = soup.find_all("div",{'class','s2TyX ueVdTc'})
        for key in keys:
            if key.text:
                keywords.append(key.title)
                print('>> get related keyword.."{text}"'.format(text=key.text))
        keys = soup.find_all("div", {"class": "s75CSd OhScic AB4Wff"})
        for key in keys:
            if key.text:
                keywords.append(key.text)
                print('>> get related keyword.."{text}"'.format(text=key.text))
        return keywords

    def google_search(self,query):
        print('>> api calling start...')
        req = self.get_results(query)
        if req['status'] == 'failed':
            return{'status':'failed'},400
        response = req['req']
        try:
            with open(f"html/{re.sub('[^A-Za-z0-9]+', '', query)}.html", "w",encoding="utf-8") as file:
                file.write(response.text)
        except Exception as e:
            print(e)
            pass
        feature_snippet = self.parse_results(response)
        dictionary = self.get_dictionary(response)
        popular_products = self.get_popular_products(response)
        top_sights = self.get_top_sights(response)
        videos = self.get_videos(response)
        oraganic = self.get_oraganic(response)
        soup = BeautifulSoup(response.content, "lxml")
        faqs = None
        if self.add_faqs == 'yes':
            faqs = self.extractQuestionData(response)
        information = self.extract_information(soup)
        rel_keywords = self.get_rel_keywords(response)
        direct_ans = {}
        try:
            direct = soup.find("div", {"class": "kp-header"})
            direct_ans = {
                'bread' : direct.find("span", "GzssTd").text,
                'crumbs' : direct.find("span", "qLLird").text,
                'answer' : direct.find('a').text,
                'link' : 'https://www.google.com{}'.format(direct.find('a')['href'])
            }
        except Exception as e:
            logger.error('error occured.{}'.format(str(e)))
            pass

        print('>> api calling end...')
        return {
            "keyword":query,
            'direct_ans':direct_ans,
            'unit_converter':feature_snippet['unit_converter'],
            "meta_description":feature_snippet['output'],
            "people_also_ask":faqs,
            "knowledge_panel":information,
            "related_keywords":rel_keywords,
            'dictionary':dictionary,
            'popular_products':popular_products,
            'top_sights':top_sights,
            'videos':videos,
            'oraganic':oraganic
            }

    


