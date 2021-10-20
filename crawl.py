from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from g_crawler import GCrawler

app = Flask(__name__)
api = Api(app)

api.add_resource(GCrawler, '/search') 

if __name__ == '__main__':
    app.run()  # run our Flask app