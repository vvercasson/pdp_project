from analysis_gui.forms.common import *
from analysis_gui.forms import common
from analysis_gui.forms.figure_form import FigureForm
import textwrap

class SunburstForm(FigureForm):
    def __init__(self):
        super().__init__(
            layout=Layout(grid_gap="40px"),
            output=Output(),
            default_font_size=12,
            default_figure_width=600,
            default_figure_height=600
        )
    
    def init(self, **kwargs):
        #replacing some wordings
        args = self._parse_kwargs("df", **kwargs)
        df = self.break_columns(args["df"])
        path = []
        if np.sum(df.Subcategory.isna()) != df.shape[0] : # with category and subcategory
            path = ['Category', 'Subcategory', 'Symptom']
        elif np.sum(df.Category.isna()) != df.shape[0] : # with category only
            path = ['Category', 'Symptom']
            
        if path:
            fig = px.sunburst(df, path=path, values='sum_symptoms',color_discrete_sequence = px.colors.qualitative.Pastel)
            fig.update_layout(margin = dict(t=0, l=0, r=0, b=0), font_size=11, width=self._default_figure_width, height=self._default_figure_height)
            fig.update_traces(insidetextorientation='radial')
            fig.update_traces(hovertemplate='sum_symptom: %{value}')
            
            self._figure=go.FigureWidget(fig)
            self._show_interface()
        else : 
            self.children = [self._output]
            with self._output:
                clear_output()
                print("No category -> no sunburst plot")
                
    def break_columns(self, df, max_length = 16):
        categories = []
        subcategories = []
        symptoms = []
        
        if np.sum(df.Category.isna()) != df.shape[0] :
            categories = df.Category.unique().tolist()
        if np.sum(df.Subcategory.isna()) != df.shape[0] :
            subcategories = df.Subcategory.unique().tolist()
        if np.sum(df.Symptom.isna()) != df.shape[0] :
            symptoms = df.Symptom.unique().tolist()
        
        for string in categories + subcategories + symptoms:
            df.replace(string, "<br>".join(textwrap.wrap(string, width=max_length)), inplace = True)
            
        return df
