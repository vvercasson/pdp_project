from .common import *
from . import common
from .figure_form import FigureForm
import numpy as np


class JaccardHeatmap(FigureForm):
    def __init__(self):
        super().__init__(
            layout=Layout(
                grid_gap="20px",
                align_items="flex-start",
                overflow="visible",
                width="max-content"
            ),
            output=Output()
        )
        
    def init(self):
        ###
        # Plotting it as a heatmap
        ###
        fig = px.imshow(pd.DataFrame(np.round(common.jaccard_table,3), # rounding values for the plot
                                    index = common.jaccard_table.index,
                                    columns= common.jaccard_table.columns),
                        text_auto=True, # annotating values in the plot
                        color_continuous_scale= 'Portland'# more color palettes available here : https://plotly.com/python/builtin-colorscales/
        )
        self._figure = go.FigureWidget(fig)
        self._figure.update_xaxes(side="top")
        self._figure.update_layout(
            autosize=False,
            width=600,
            height=600
            )
        #fig.write_image("figure5_heatmap_jaccard.pdf") # writting the figure into a file
        # self._figure.show() # showing figure
        
        self._show_interface([])