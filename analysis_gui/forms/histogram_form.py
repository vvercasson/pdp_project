from .common import *
from . import common
from .palette_figure_form import PaletteFigureForm
from ipywidgets import ToggleButtons

class HistogramUI(PaletteFigureForm):
    
    def __init__(self):
        super().__init__(
            layout=Layout(
                grid_gap="15px"
            ),
            default_figure_width=1067,
            default_figure_height=600
        )
        self._df_questionnaires = None
        # self._sortBy = "Symptom"
        
        self._sortBy =ToggleButtons(
            options=[('Occurences', 'Symptom'), ('Category', 'Category')],
            description='Sort by ',
            disabled=False,
            button_style='',
            tooltips=['Sort by number of occurences', 'Sort by category and by occurences'],
            layout=Layout(display='flex', flex_flow="row", grid_gap="5px")
        )
        
        self._sortBy.observe(self._sort_by, names=["value"])
        
    def init(self, **kwargs):
        args = self._parse_kwargs("df", "references", **kwargs)
        df, references = args["df"], args["references"]
        
        self._df_questionnaires = df.drop(references, axis = 1).sort_values(by=['sum_symptoms', 'Ab'], ascending=[False,True])
        if df.shape[0] != df['Category'].isnull().sum(): 
            color = 'Category'
            self._sortBy.disabled = False
            self._colorPicker.disabled = False
        else: 
            color = 'sum_symptoms'
            self._sortBy.disabled = True
            self._colorPicker.disabled = True
            
        bar = px.bar(
            self._df_questionnaires,
            x='Symptom',
            y='sum_symptoms',
            color=color,
            labels={'sum_symptoms':'Number of questionnaires'},
            color_discrete_sequence=common._palettes.get(self._default_palette),
            category_orders = {'Category':self._df_questionnaires.sort_values(by='Ab').Category.unique()}
        )
        
        self._figure = go.FigureWidget(bar)
        self._figure.update_layout(xaxis_tickangle=-60, autosize=True, height=self._default_figure_height, width=self._default_figure_width)
        self._figure.update_layout(xaxis={'categoryorder':'array', 'categoryarray': self._df_questionnaires[self._sortBy.value].unique()})
        
        self._show_interface([self._sortBy])
        
    def _sort_by(self, sortBy):
        order = self._df_questionnaires[sortBy["new"]].unique()
        if sortBy["new"] == 'Category':
            order = np.setdiff1d(order, self._df_questionnaires['Symptom'].unique())
        self._figure.update_layout(xaxis={'categoryorder':'array', 'categoryarray': order})
        
    def _change_color_palette(self, palette):
        # print(self._figure.data)
        colors = cycle(common._palettes.get(palette["new"]))
        for bar in self._figure.data:
            bar.update(marker={'color' : next(colors)})