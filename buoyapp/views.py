import numpy as np
import xarray as xr
import pandas as pd
import itertools

from flask import Blueprint
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, CDSView, DataTable, DateFormatter, TableColumn, CustomJS, DatePicker, TextInput, LabelSet, HoverTool, NumeralTickFormatter, Select
from bokeh.models.widgets import CheckboxGroup, NumberFormatter
from bokeh.io import show, curdoc
from bokeh.layouts import column, row, grid, WidgetBox
from datetime import date
from bokeh.palettes import YlGnBu9 as palette

from bs4 import BeautifulSoup
import requests

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # ------------------------------------------------------------------------------
    # Widget: Text Input for Buoy Number
    # ------------------------------------------------------------------------------
    buoy_input = TextInput(value='44066', title="Buoy ID Number", name="buoy_input")
    buoy_input.on_change("value", update_plot)

    #dropdown = Select(title="Select a Buoy", value="Select", options=buoys, name="buoy_input")
    #dropdown.on_change("value", update_plot)

    # ------------------------------------------------------------------------------
    # Widget: Data Table
    # ------------------------------------------------------------------------------
    formatter = NumberFormatter(format='0.000')

    columns = [
        TableColumn(field="time", title="Time", formatter=DateFormatter()),
        TableColumn(field="air_temperature", title="Air Temperature (°C)", formatter=formatter),
        TableColumn(field="sea_surface_temperature", title="Sea Surface Temperature (°C)", formatter=formatter),
        TableColumn(field="dewpt_temperature", title="Dew Point Temperature (°C)", formatter=formatter),
        TableColumn(field="air_pressure", title="Air Pressure (hPa)", formatter=formatter),
        TableColumn(field="mean_wave_dir", title="Mean Wave Direction (degT)", formatter=formatter),
        TableColumn(field="wind_dir", title="Wind Direction (°C)", formatter=formatter),
        TableColumn(field="wind_spd", title="Wind Speed (m/s)", formatter=formatter),
        TableColumn(field="gust", title="Gust (m/s)", formatter=formatter),
    ]

    # ------------------------------------------------------------------------------
    # Widget: Date Pickers
    # ------------------------------------------------------------------------------
    start_date_picker = DatePicker(title='Start date', value='2021-07-24', name="start_date")
    start_date_picker.on_change("value", update_plot)

    end_date_picker = DatePicker(title='End date', value=date.today(), name="end_date")
    end_date_picker.on_change("value", update_plot)

    source = find_dataset(buoy_input = buoy_input.value,
                          start_date = start_date_picker.value,
                          end_date = end_date_picker.value)

    return "<h1>Heroku Test</h1>"


# ------------------------------------------------------------------------------
# Function: Load dataset from NDBC Thredds server
# ------------------------------------------------------------------------------
def find_dataset(buoy_input, start_date, end_date):
    data_url = 'https://dods.ndbc.noaa.gov/thredds/dodsC/data/stdmet/' + buoy_input + '/' + buoy_input + '.ncml'
    ds = xr.open_dataset(data_url)
    ds = ds.sel(time=slice(start_date, end_date))
    df = ds.to_dataframe().reset_index().set_index('time')
    source = ColumnDataSource(df)

    print("url: " + data_url)
    print("Data has been found for buoy #" + buoy_input)

    return source
