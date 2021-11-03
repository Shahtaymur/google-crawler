import people_also_ask
import json
import requests
import urllib
import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
#import urllib.request as urllib
from flask_restful import Resource, Api, reqparse
from flask import request
from random import choice
import config

# with open('browser_agents.txt', 'r') as file_handle:
#     USER_AGENTS = file_handle.read().splitlines()

# DEFAULT_HEADERS = [
#             ('User-Agent', choice(USER_AGENTS)),
#             ("Accept-Language", "en-US,en;q=0.5"),
#         ]
# SEARCH_URL = "https://google.com/search"
class GCrawler(Resource):

    # def __init__(self,query) -> None:
    #     self.query = query
    #     self.result = self.google_search(self.query)
       
    def get(self):
        q_string = request.args.get('q')
        add_faqs = request.args.get('faqs')
        if not q_string:
            return {'message': "invalid request pls add search para and try again.. e.g http://127.0.0.1:5000/search?q=apple"}, 405
        self.query = q_string
        self.add_faqs = add_faqs
        self.result =  self.google_search(self.query)
        # with open(f'{self.query}.json', 'w', encoding ='utf8') as json_file:
        #     json.dump(self.result, json_file, ensure_ascii = False)
        return {'data': self.result}, 200

    def get_source(self,url):
        """Return the source code for the provided URL. 

        Args: 
            url (string): URL of the page to scrape.

        Returns:
            response (object): HTTP response object from requests_html. 
        """

        try:
            session = HTMLSession()
            time.sleep(0.5)
            proxy = {"http":"http://{}:{}@{}".format(config.PROXY_USER, config.PROXY_PASS, config.GEONODE_DNS)}
            #r = requests.get(url , proxies=proxy)
            response = session.get(url,proxies=proxy)
            if response.status_code != 200:
                exit({"message":"someting wrong pls try again later"})
            session.close()
            return response

        except requests.exceptions.RequestException as e:
            print(e)

    def scrape_google(self,query):

        #query = urllib.parse.quote_plus(query)
        response = self.get_source(query)

        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                        'https://google.', 
                        'https://webcache.googleusercontent.', 
                        'http://webcache.googleusercontent.', 
                        'https://policies.google.',
                        'https://support.google.',
                        'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)

        return links

    def get_results(self,query):
        
        query = urllib.parse.quote_plus(query)
        response = self.get_source('https://www.google.com/search?q='+query)
        # headers = {
        #     "User-Agent":
        #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
        # }

        # params = {
        #     'q': query,
        #     'hl': 'en',
        #     'num': '100'
        # }
        # response = requests.get("https://www.google.com/search", headers=headers, params=params)
        #time.sleep(2)
        return response
        
    def parse_results(self,response):
        
        css_identifier_result = ".tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".IsZvec"
        results = response.html.find(css_identifier_result)
        feature_snippet = response.html.find('h2')
         
        output = []
        answer = []
        unit_converter = {}
        for snippet in feature_snippet:
            if snippet.full_text == "Featured snippet from the web":
                answer.append(people_also_ask.get_related_answer(self.query,True))
                break
            elif snippet.full_text == "Unit converter":
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
                    except:
                        pass
                
        for i,result in enumerate(results):
            print('>> get meta description...')
            item = {}
            item['title'] = result.find(css_identifier_title, first=True).text
            item['link'] = result.find(css_identifier_link, first=True).attrs['href']
            if i == 0 and len(answer) > 0 and not answer == '':
                item['snippet'] = answer[0]
            else:
                meta_description = result.find(css_identifier_text, first=True)
                table  = meta_description.find('table')
                if table:
                    try:
                        soup = BeautifulSoup(result.html,"html.parser")
                        tr = soup.find_all('tr')
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
                        item['meta_data'] = {'columns':header,'values':values}
                    except:
                        pass
                item['text'] = meta_description.text
            
            output.append(item)
        return {'output':output,'unit_converter':unit_converter}

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
                            except:
                                pass
                    dfn['dictionary'].append(dfnlist)
            except:
                pass
        return dfn

    def get_popular_products(self,response):
        soup = BeautifulSoup(response.text,"html.parser")
        cards = soup.find('g-scrolling-carousel')
        cards_list = {'popular_products':[]}
        if cards:
            cards = cards.find_all('div',{'class','WGwSK SoZvjb'})
            for card in cards:
                cards_list['popular_products'].append(card.text)
                
        return cards_list

    def get_top_sights(self,response):
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
                    except:
                        pass

        return top_list

    def get_videos(self,response):
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
                    except:
                        pass
                    if not title == None:
                        item = {
                            'link' : link,
                            'title' : title,
                            'date' : date,
                            'raw_data' : raw_data
                        }
                        video_list['data'].append(item)
                except:
                    pass

        return video_list

    def get_oraganic(self,response):
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
                    except:
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
                    pass

        return recip_list

    #people_alse_ask
    def extractQuestionData(self,keyword):
        data = []
        print('>> get related questions..')
        rel_questions = people_also_ask.get_related_questions(keyword)
        for question in rel_questions:
            title = question.split('Search for:')[0]
            #time.sleep(0.5)
            answer = people_also_ask.get_related_answer(title,True)
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
            information['description'] = description.lower().replace("\n","")
            for attribute in attributes:
                if(attribute.text):
                    info = attribute.text.split(":",1)
                    information['attributes'].append({'key':info[0].lower().replace("\n",""),'value':info[1].lower().replace("\n","")})
        except:
            pass
        return information

    def get_rel_keywords(self,response):
        print('>> get related keyword...')
        soup = BeautifulSoup(response.text,"html.parser")
        keywords = []
        keys = soup.find_all("div",{"class":"M7lz2c XC18Gb diAzE"})
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
        response = self.get_results(query)
        feature_snippet = self.parse_results(response)
        dictionary = self.get_dictionary(response)
        popular_products = self.get_popular_products(response)
        top_sights = self.get_top_sights(response)
        videos = self.get_videos(response)
        oraganic = self.get_oraganic(response)
        soup = BeautifulSoup(response.content, "lxml")
        faqs = self.extractQuestionData(query)
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
        except:
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

    


