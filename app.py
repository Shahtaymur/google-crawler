from flask import Flask
from flask_restful import Resource, Api, reqparse
from numpy import true_divide
import pandas as pd
import ast
from g_crawler import GCrawler

app = Flask(__name__)
api = Api(app)

api.add_resource(GCrawler, '/search') 

if __name__ == '__main__':
    app.run(threaded=True,debug=True,host='127.0.0.1', port=5002)  # run our Flask app