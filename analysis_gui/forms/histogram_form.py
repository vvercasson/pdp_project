from .common import *
from . import common
from .figure_form import FigureForm
from ipywidgets import  Checkbox, GridBox, ToggleButtons

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
            value='Pastel',
            description="Color Palette",
            disabled=False
        )
        
        self._sortBy =ToggleButtons(
            options=[('Occurences', 'Symptom'), ('Category', 'Category')],
            description='Sort by: ',
            disabled=False,
            button_style='',
            tooltips=['Sort by number of occurences', 'Sort by category and by occurences']
        )
        
    def init(self):
        self._name = "histo"
        self._output = interactive_output(self.update, {'palette': self._colorPicker, "sortBy": self._sortBy})
        self._output.layout.width = "100%"
        children = [
            HBox(
                children=[self._sortBy, self._colorPicker],
                layout=Layout(width="100%")
            ),
            HBox(
                children=[self._output],
                layout=Layout(width="95%", justify_content="space-between")
            )
        ]
        self._show_interface(children)

    def update(self, sortBy, palette="Pastel"):
        self._update_figure(sortBy, palette)
        self._figure.show()
        
    def _update_figure(self, sortBy, palette):
        if self._df_questionnaires is None:
            self._df_questionnaires = common.df.drop(references, axis = 1).sort_values(by=['sum_symptoms', 'Ab'], ascending=[False,True])
            
        if self._figure is None:
            if common.df.shape[0] != common.df['Category'].isnull().sum(): 
                self._color = 'Category'
            else: 
                self._color = 'sum_symptoms'
        colors = self._palettes.get(palette)
        self._figure = px.bar(
            self._df_questionnaires,
            x='Symptom',
            y='sum_symptoms',
            color=self._color,
            labels={'sum_symptoms':'Number of questionnaires'},
            color_discrete_sequence=colors,
            category_orders = {'Category':self._df_questionnaires.sort_values(by='Ab').Category.unique()}
        )
        self._figure.update_layout(xaxis_tickangle=-60,autosize=True, height=600)
        self._figure.update_layout(xaxis={'categoryorder':'array', 'categoryarray': self._df_questionnaires[sortBy].unique()})
            