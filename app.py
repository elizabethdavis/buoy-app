import numpy as np
import xarray as xr
import pandas as pd
import itertools

from flask import Flask, render_template
from easybase import get
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput, DataTable, DateFormatter, TableColumn, CustomJS, DatePicker, LabelSet, HoverTool, NumeralTickFormatter
from bokeh.io import curdoc
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import YlGnBu9 as palette
from datetime import date

app = Flask(__name__, template_folder='buoyapp/templates')

# create empty list
buoys = []

bokeh_doc = curdoc()

tools = "pan, box_zoom, save, reset"

@app.route('/')
def index():
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

    # ------------------------------------------------------------------------------
    # Function: Create temperature plot
    # Sources: Air Temperature, Sea Surface Temperature, Dewpoint Temperature
    # Units: Degrees Celsius
    # ------------------------------------------------------------------------------
    def make_temp_plot(source, buoy_input):
        air_hover = HoverTool(
            tooltips = [
                ('Air Temp', '@air_temperature{(00.00)}'),
                ('Date', '@time{%F}')],
                formatters={'@time':'datetime'},
                names=['air_hover'],
                mode='vline')

        sea_hover = HoverTool(
            tooltips = [
                ('Sea Surface Temperature', '@sea_surface_temperature{(00.00)}'),
                ('Date', '@time{%F}')],
                formatters={'@time':'datetime'},
                names=['sea_hover'],
                mode='vline')

        dewpt_hover = HoverTool(
            tooltips = [
                ('Dew Point Temperature', '@dewpt_temperature{(00.00)}'),
                ('Date', '@time{%F}')],
                formatters={'@time':'datetime'},
                names=['dewpt_hover'],
                mode='vline')

        p = figure(plot_width = 600, plot_height = 400,
                   x_axis_label = 'Time',
                   x_axis_type = "datetime",
                   y_axis_label = 'degrees C',
                   title="Temperature",
                   name="temperature_plot",
                   sizing_mode="scale_width",
                   tools=tools)

        air = p.line(x='time', y='air_temperature', legend_label = "Air Temperature", source=source, color=palette[1], name='air_hover')
        p.add_tools(air_hover)
        sea = p.line(x='time', y='sea_surface_temperature', legend_label = "Sea Surface Temperature", source=source, color=palette[2], name='sea_hover')
        p.add_tools(sea_hover)
        dewpt = p.line(x='time', y='dewpt_temperature', legend_label = "Dew Point Temperature", source=source, color=palette[3], name='dewpt_hover')
        p.add_tools(dewpt_hover)

        p.toolbar.active_drag = None
        p.legend.click_policy = "hide"

        return p

    buoy_input = TextInput(value='44066', title="Buoy ID Number", name="buoy_input")
    start_date_picker = DatePicker(title='Start date', value='2021-07-24', name="start_date")
    end_date_picker = DatePicker(title='End date', value=date.today(), name="end_date")

    # ------------------------------------------------------------------------------
    # Create Charts
    # ------------------------------------------------------------------------------
    source = find_dataset(buoy_input = buoy_input.value,
                          start_date = start_date_picker.value,
                          end_date = end_date_picker.value)

    p = make_temp_plot(source, buoy_input = buoy_input.value)

    script, div = components(p)

    return render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')

if __name__ == "__main__":
    app.run(debug=True)
