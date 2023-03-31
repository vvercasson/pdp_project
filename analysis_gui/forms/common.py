df = None
experiment = ""
header = ['Category','Subcategory', 'Ab', 'Symptom']
references = []
col = []
cat_per_questionnaire = None
jaccard_table = None
jaccard = None
sympt_per_questionnaire = None

import pandas as pd
import numpy as np

from ipywidgets import Layout, FileUpload, Button, \
    Box, VBox, HBox, Dropdown, Output, interactive_output, \
    Text, Image, Label, HTML, IntSlider
    
from IPython.display import display, clear_output
from itertools import cycle

import chart_studio as cs
import chart_studio.plotly as py

cs.tools.set_credentials_file(username='vvercasson', api_key='qeP4TZRoVTWlnXijtZqD')

import io, inspect
import plotly.express as px
import plotly.graph_objects as go

melt_output=Output()