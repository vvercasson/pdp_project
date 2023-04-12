from .common import *
from . import common
from .figure_form import FigureForm


class JaccardHeatmap(FigureForm):
    def __init__(self):
        super().__init__(
            layout=Layout(
                grid_gap="20px",
                align_items="flex-start",
                overflow="visible",
                width="max-content"
            ),
            default_figure_height=600,
            default_figure_width=600
        )
        
    def init(self, **kwargs):
        args = self._parse_kwargs("jaccard_table", **kwargs)
        jaccard_table = args["jaccard_table"]
        ###
        # Plotting it as a heatmap
        ###
        fig = px.imshow(pd.DataFrame(np.round(jaccard_table,3), # rounding values for the plot
                                    index = jaccard_table.index,
                                    columns= jaccard_table.columns),
                        text_auto=True, # annotating values in the plot
                        color_continuous_scale= 'Portland'# more color palettes available here : https://plotly.com/python/builtin-colorscales/
        )
        self._figure = go.FigureWidget(fig)
        self._figure.update_xaxes(side="top")
        self._figure.update_layout(
            autosize=False,
            width=self._default_figure_width,
            height=self._default_figure_height
        )
        #fig.write_image("figure5_heatmap_jaccard.pdf") # writting the figure into a file
        # self._figure.show() # showing figure
        
        self._show_interface()