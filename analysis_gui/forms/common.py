df = None
experiment = ""
header = ['Category','Subcategory', 'Ab', 'Symptom']
references = []
col = []

import pandas as pd

from ipywidgets import Layout, FileUpload, Button, \
    Box, VBox, HBox, Dropdown, Output, interactive_output, \
    Text, Image, Label, HTML
    
from IPython.display import display, display_html
from itertools import cycle

import io, inspect
import plotly.express as px
import plotly.graph_objects as go