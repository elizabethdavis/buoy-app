import numpy as np
import xarray as xr
import pandas as pd
import itertools

from flask import Blueprint
from flask import Flask
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, CDSView, DataTable, DateFormatter, TableColumn, CustomJS, DatePicker, TextInput, LabelSet, HoverTool, NumeralTickFormatter, Select
from bokeh.models.widgets import CheckboxGroup, NumberFormatter
from bokeh.io import show, curdoc
from bokeh.layouts import column, row, grid, WidgetBox
from datetime import date
from bokeh.palettes import YlGnBu9 as palette

from bs4 import BeautifulSoup
import requests

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'buoy-explore-app'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
