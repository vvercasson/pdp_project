from analysis_gui.forms.common import *
from analysis_gui.forms import common
from analysis_gui.forms.figure_form import FigureForm

class SunburstForm(FigureForm):
    def __init__(self):
        super().__init__(layout=Layout(grid_gap="20px"),
            output=Output()
        )
    
    def init(self):
        #replacing some wordings
        df = self.break_columns()
        path = []
        if np.sum(df.Subcategory.isna()) != df.shape[0] : # with category and subcategory
            path = ['Category', 'Subcategory', 'Symptom']
        elif np.sum(df.Category.isna()) != df.shape[0] : # with category only
            path = ['Category', 'Symptom']
            
        if path:
            fig = px.sunburst(df, path=path, values='sum_symptoms',color_discrete_sequence = px.colors.qualitative.Pastel)
            fig.update_layout(margin = dict(t=0, l=0, r=0, b=0), font_size=11, width=600, height=600)
            fig.update_traces(insidetextorientation='radial')
            fig.update_traces(hovertemplate='sum_symptom: %{value}')
            
            self._figure=go.FigureWidget(fig)
            self._show_interface([])
        else : 
            self.children = [self._output]
            with self._output:
                clear_output()
                print("No category -> no sunburst plot")
                
    def break_columns(self, max_length = 16):
        df = common.df.copy()
        categories = []
        subcategories = []
        symptoms = []
        
        if np.sum(common.df.Category.isna()) != common.df.shape[0] :
            categories = common.df.Category.unique().tolist()
        if np.sum(common.df.Subcategory.isna()) != common.df.shape[0] :
            subcategories = common.df.Subcategory.unique().tolist()
        if np.sum(common.df.Symptom.isna()) != common.df.shape[0] :
            symptoms = common.df.Symptom.unique().tolist()
        
        for string in categories + subcategories + symptoms:
            tokens = string.strip().split(" ")
            broken = tokens
            length = 0
            index = 0
            for token in tokens:
                length += len(token) + 1
                index += 1
                if length >= max_length :
                    if abs(max_length - length) < abs(max_length - (length - len(token))):
                        broken.insert(index, "<br>")
                    else:
                        broken.insert(index-1, "<br>")
                    length = 0
            df.replace(string, " ".join(broken).replace(" <br> ", "<br>").replace(" <br>", "<br>"), inplace = True)
            
        return df
