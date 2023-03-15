df = None
experiment = ""
header = ['Category','Subcategory', 'Ab', 'Symptom']
references = []

import pandas as pd

from ipywidgets import Layout, FileUpload, Button, \
    Box, VBox, HBox, Dropdown, Output, interactive_output, \
    Text, Image, HTML, Label
    
from IPython.display import display, Javascript
from itertools import cycle

import io, inspect, os, base64
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio