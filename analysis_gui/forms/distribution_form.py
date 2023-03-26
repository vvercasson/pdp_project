from .common import *
from . import common
from .figure_form import FigureForm
import plotly.express as px
from sklearn.preprocessing import normalize

class DistributionUI(FigureForm):
    def __init__(self):
        super().__init__(
            layout=Layout(grid_gap="20px"),
            output=Output()
        )
        
    def init(self):
        if common.df.shape[0] != common.df['Category'].isnull().sum() : 
            fig = px.imshow(pd.DataFrame(np.round(normalize(common.cat_per_questionnaire,norm='l1').T*100,1), # for printing text, we round the percentages to 1 decimal
                                        columns = common.cat_per_questionnaire.index,
                                        index= common.cat_per_questionnaire.columns),
                            text_auto=True, # add the text
                            color_continuous_scale= 'Portland'# more color palettes available here : https://plotly.com/python/builtin-colorscales/
            )
            self._figure = go.FigureWidget(fig)
            self._figure.update_xaxes(side="top") # xaxis on top of the figure
            self._figure.update_layout(
                autosize=False,
                width=800,
                height=400
                )
            
            self._show_interface([])
            # fig.write_image("figure3_heatmap.pdf") # writing the figure in a file
            #fig.show() # showing the figure
        else: 
            self.children = [self._output]
            with self._output:
                clear_output()
                print('No category in this dataframe !')
            
            
            