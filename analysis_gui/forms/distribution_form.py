from .common import *
from . import common
from .figure_form import FigureForm
import plotly.express as px
from sklearn.preprocessing import normalize

class DistributionUI(FigureForm):
    def __init__(self):
        super().__init__(
            layout=Layout(grid_gap="20px"),
            default_figure_width=800,
            default_figure_height=400
        )
        
    def init(self, **kwargs):
        args = self._parse_kwargs("df", "cat_per_questionnaire", **kwargs)
        df, cat_per_questionnaire = args["df"], args["cat_per_questionnaire"]
        if df.shape[0] != df['Category'].isnull().sum() : 
            fig = px.imshow(pd.DataFrame(np.round(normalize(cat_per_questionnaire,norm='l1').T*100,1), # for printing text, we round the percentages to 1 decimal
                                        columns = cat_per_questionnaire.index,
                                        index= cat_per_questionnaire.columns),
                            text_auto=True, # add the text
                            color_continuous_scale= 'Portland'# more color palettes available here : https://plotly.com/python/builtin-colorscales/
            )
            self._figure = go.FigureWidget(fig)
            self._figure.update_xaxes(side="top") # xaxis on top of the figure
            self._figure.update_layout(
                autosize=False,
                width=self._default_figure_width,
                height=self._default_figure_height
            )
            
            self._show_interface()
            # fig.write_image("figure3_heatmap.pdf") # writing the figure in a file
            #fig.show() # showing the figure
        else: 
            self.children = [self._output]
            with self._output:
                clear_output()
                print('No category in this dataframe !')
            
            
            