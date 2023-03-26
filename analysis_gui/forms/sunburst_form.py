from .common import *
from . import common
from .figure_form import FigureForm

class SunburstForm(FigureForm):
    def __init__(self):
        super().__init__(layout=Layout(grid_gap="20px"),
            output=Output()
        )
    
    def init(self):
        #replacing some wordings
        if common.experiment == "Gauld2023_OSAS_content_analysis" : 
            common.df.replace("Stop breathing observations","Stop breathing <br> observations", inplace = True)
            common.df.replace("Self-complaints of breath abnormalities","Self-complaints of <br> breath abnormalities", inplace = True)
            common.df.replace("Breath abnormalities complaints reported by other","Breath abnormalities <br> complaints reported <br> by other", inplace = True)
            common.df.replace("Sociodemographic","Sociodem.", inplace = True)
            common.df.replace("Anthropometry","Antropo.", inplace = True)
            common.df.replace("Sleep-related symptoms","Sleep-related <br> symptoms", inplace = True)
            common.df.replace("Breath abnormalities complaints","Breath abn. compl.", inplace = True)
            common.df.replace("OSA symptoms","OSA <br> symptoms", inplace = True)
            common.df.replace("Clinical characteristics","Clinical <br> characteristics", inplace = True)
            common.df.replace("Breath abnormalities observations","Breath <br> abnormalities <br> observations", inplace = True)
            common.df.replace("Breath abnormalities-related complaints","Breath <br> abnormalities-related <br> complaints", inplace = True)
        if np.sum(common.df.Subcategory.isna()) != common.df.shape[0] : # with category and subcategory
            fig = px.sunburst(common.df, path=['Category', 'Subcategory', 'Symptom'], values='sum_symptoms',color_discrete_sequence = px.colors.qualitative.Pastel)
            fig.update_layout(margin = dict(t=0, l=0, r=0, b=0), font_size=11, width =600, height = 600)
            fig.update_traces(insidetextorientation='radial')
            fig.update_traces(hovertemplate='sum_symptom: %{value}')
            #fig.write_image("figure6_sunburst_plot.pdf") # writting the figure into a file
            self._figure=go.FigureWidget(fig)
        elif np.sum(common.df.Category.isna()) != common.df.shape[0] : # with category only
            fig = px.sunburst(common.df, path=['Category', 'Symptom'], values='sum_symptoms',color_discrete_sequence = px.colors.qualitative.Pastel)
            fig.update_layout(margin = dict(t=0, l=0, r=0, b=0), font_size=11, width =600, height = 600)
            fig.update_traces(insidetextorientation='radial')
            fig.update_traces(hovertemplate='sum_symptom: %{value}')
            #fig.write_image("figure6_sunburst_plot.pdf") # writting the figure into a file
            self._figure=go.FigureWidget(fig)
        else : 
            print("No category -> no sunburst plot")
        self._show_interface([])