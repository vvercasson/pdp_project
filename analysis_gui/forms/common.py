df = None
experiment = ""
header = ['Category','Subcategory', 'Ab', 'Symptom']
references = []
col = []
cat_per_questionnaire = None
jaccard_table = None

import pandas as pd

from ipywidgets import Layout, FileUpload, Button, \
    Box, VBox, HBox, Dropdown, Output, interactive_output, \
    Text, Image, Label, HTML, IntSlider
    
from IPython.display import display, clear_output
from itertools import cycle

import io, inspect
import plotly.express as px
import plotly.graph_objects as go

melt_output=Output()