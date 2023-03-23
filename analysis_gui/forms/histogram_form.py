from .common import *
from . import common
from .figure_form import FigureForm
from ipywidgets import ToggleButtons

class HistogramUI(FigureForm):
    
    def __init__(self):
        super().__init__(
            layout=Layout(grid_gap="20px"),
            output=Output()
        )
        self._palettes = px.colors.qualitative.__dict__.copy()
        self._df_questionnaires = None
        # self._sortBy = "Symptom"
        
        self._colorPicker = Dropdown(
            options=[name for name, body 
                     in inspect.getmembers(px.colors.qualitative)
                     if isinstance(body, list) and name != "__all__" and not name.endswith("_r")],
            value='D3',
            description="Color Palette",
            disabled=False
        )
        
        self._sortBy =ToggleButtons(
            options=[('Occurences', 'Symptom'), ('Category', 'Category')],
            description='Sort by ',
            disabled=False,
            button_style='',
            tooltips=['Sort by number of occurences', 'Sort by category and by occurences'],
            layout=Layout(display='flex', flex_flow="row", grid_gap="5px")
        )
        
    def init(self):
        self._df_questionnaires = common.df.drop(references, axis = 1).sort_values(by=['sum_symptoms', 'Ab'], ascending=[False,True])
            
        if common.df.shape[0] != common.df['Category'].isnull().sum(): 
            self._color = 'Category'
        else: 
            self._color = 'sum_symptoms'
            
        if self._figure is None and common.df.shape[0] != common.df['Category'].isnull().sum():
            self._sortBy.observe(self._sort_by, names=["value"])
            self._colorPicker.observe(self._change_color_palette, names=["value"])
        else :
            self._sortBy.disabled = True
            self._colorPicker.disabled = True
            
        bar = px.bar(
            self._df_questionnaires,
            x='Symptom',
            y='sum_symptoms',
            color=self._color,
            labels={'sum_symptoms':'Number of questionnaires'},
            color_discrete_sequence=self._palettes.get(self._colorPicker.value),
            category_orders = {'Category':self._df_questionnaires.sort_values(by='Ab').Category.unique()}
        )
        self._figure = go.FigureWidget(bar)
        self._figure.update_layout(xaxis_tickangle=-60, autosize=True, height=600)
        self._figure.update_layout(xaxis={'categoryorder':'array', 'categoryarray': self._df_questionnaires[self._sortBy.value].unique()})
        
        # self._output = interactive_output(self.update, {'palette': self._colorPicker, "sortBy": self._sortBy})
        # self._output.layout.width = "100%"
        children = [
            HBox(
                children=[self._sortBy, self._colorPicker],
                layout=Layout(width="100%", grid_gap="10px")
            )
        ]
        self._show_interface(children)
        
    def _sort_by(self, sortBy):
        # print(sortBy["new"])
        self._figure.update_layout(xaxis={'categoryorder':'array', 'categoryarray': self._df_questionnaires[sortBy["new"]].unique()})
        
    def _change_color_palette(self, palette):
        print(self._figure.data)
        colors = cycle(self._palettes.get(palette["new"]))
        for bar in self._figure.data:
            bar.update(marker={'color' : next(colors)})
        pass   