from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from elasticsearch import Elasticsearch
import pandas as pd 


#Configure and initalize app
app = Flask(__name__)
app.config.from_object(Config)
app.config['TEMPLATES_AUTO_RELOAD'] = True
bootstrap = Bootstrap(app)

from app import routes