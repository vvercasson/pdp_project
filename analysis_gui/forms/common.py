header = ['Category','Subcategory', 'Ab', 'Symptom']

import pandas as pd
import numpy as np

from ipywidgets import Layout, FileUpload, Button, \
    VBox, HBox, TwoByTwoLayout, Dropdown, Output, interactive_output, \
    Text, Image, Label, HTML, IntSlider
    
from IPython.display import display, clear_output
from itertools import cycle

import io, inspect
import plotly.express as px
import plotly.graph_objects as go
from copy import deepcopy, copy

melt_output=Output()