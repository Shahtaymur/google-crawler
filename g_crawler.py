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
from contextlib import closing

with open('browser_agents.txt', 'r') as file_handle:
    USER_AGENTS = file_handle.read().splitlines()

DEFAULT_HEADERS = [
            ('User-Agent', choice(USER_AGENTS)),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]
SEARCH_URL = "https://google.com/search"
class GCrawler(Resource):

    # def __init__(self,query) -> None:
    #     self.query = query
    #     self.result = self.google_search(self.query)
       
    def get(self):
        q_string = request.args.get('q')
        if not q_string:
            return {'message': "invalid request pls add search para and try again.. e.g http://127.0.0.1:5000/search?q=apple"}, 405
        self.query = q_string
        self.result =  self.google_search(self.query)
        with open(f'{self.query}.json', 'w', encoding ='utf8') as json_file:
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
            # opener = urllib.build_opener()
            # opener.addheaders = DEFAULT_HEADERS
            # with closing(opener.open(SEARCH_URL +
            #                  "?hl=en&q="+ urllib.quote(url))) as response:
                # soup = BeautifulSoup(response.read(), "lxml")
                #return response.read()
            session = HTMLSession()
            time.sleep(2)
            response = session.get(url)
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
        #soup = BeautifulSoup(response.text,"html.parser")
        css_identifier_result = ".tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = ".yuRUbf a"
        css_identifier_text = ".IsZvec"
        results = response.html.find(css_identifier_result)

        output = []
        for result in results:
            print('>> get feature snippet...')
            item = {
                'title': result.find(css_identifier_title, first=True).text,
                'link': result.find(css_identifier_link, first=True).attrs['href'],
                'text': result.find(css_identifier_text, first=True).text
            }
            output.append(item)
            
        return output

    #people_alse_ask
    def extractQuestionData(self,keyword):
        data = []
        print('>> get related questions..')
        rel_questions = people_also_ask.get_related_questions(keyword)
        for question in rel_questions:
            title = question.split('Search for:')[0]
            time.sleep(0.5)
            answer = people_also_ask.get_related_answer(title,True)
            data.append(answer)
            print('>> get related answer of "{question}" - "{answer}"'.format(question=title,answer=answer))
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

    def get_rel_keywords(self,soup:BeautifulSoup):
        print('>> get related keyword...')
        keywords = []
        keys = soup.find_all("a",attrs={"class":"exp-r"})
        for key in keys:
            if key.text:
                keywords.append(key.text)
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
        #soup = BeautifulSoup(response.content, "html.parser")
        soup = BeautifulSoup(response.content, "lxml")
        
        faqs = self.extractQuestionData(query)
        information = self.extract_information(soup)
        rel_keywords = self.get_rel_keywords(soup)
        feature_snippet = self.parse_results(response)
        print('>> api calling end...')
        return {
            "keyword":query,
            "feature_snippet":feature_snippet,
            "people_also_ask":faqs,
            "info":information,
            "related_keywords":rel_keywords
            }

    


