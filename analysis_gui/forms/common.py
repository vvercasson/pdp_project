header = ['Category','Subcategory', 'Ab', 'Symptom']

import pandas as pd
import numpy as np
import os, base64


from ipywidgets import Layout, FileUpload, Button, \
    VBox, HBox, TwoByTwoLayout, Dropdown, Output, \
    Text, Image, Label, HTML, IntSlider
    
from IPython.display import display, clear_output, Javascript
from itertools import cycle

import io, inspect
import plotly.express as px
import plotly.graph_objects as go
from copy import deepcopy, copy

def filter_palettes(pair):
    key, value = pair
    # print(key)
    return isinstance(value, list) and key != "__all__" and not key.endswith("_r")

melt_output=Output()
_palettes = dict(filter(filter_palettes, px.colors.qualitative.__dict__.items()))

TYPE_XSL = "application/vnd.ms-excel"
TYPE_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

mime_types = {
    "xls": TYPE_XSL,
    "xlsx": TYPE_XLSX,
    "csv": "text/csv"
}

with open("resources/loading.gif", 'rb') as img:
    loading_gif = img.read()