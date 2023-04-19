from analysis_gui.forms.palette_figure_form import PaletteFigureForm
from .common import *
import analysis_gui.forms.common as common
from ipywidgets import FloatSlider

class CircleForm(PaletteFigureForm):
    
    def __init__(self):     
        super().__init__(
            output=Output(width="fit-content"),
            layout= Layout(
                width="max-content",
                grid_gap="10px",
                align_items="flex-start",
                overflow="visible"
            ),
            default_figure_height=600,
            default_figure_width=600,
            default_font_size=10
        )
        self._default_min_radius = 6
        self._default_max_radius = 20
        
        self._max_radius = IntSlider(
            value=self._default_max_radius,
            min=6,
            max=50,
            step=1,
            description='Max Radius :',
            disabled=False,
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
        
        self._min_radius = FloatSlider(
            value=self._default_min_radius,
            min=1,
            max=25,
            step=0.2,
            description='Min Radius :',
            disabled=False,
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
        )

    def init(self, **kwargs):
        if self._figure is None:
            self._max_radius.observe(self._update_radius, names=["value"])
            self._min_radius.observe(self._update_min_radius, names=["value"])
        args = self._parse_kwargs("df", "col", **kwargs)
        self._df = args["df"]
        self._col = args["col"]
        self._init_circle()
        
        self._show_interface([self._max_radius, self._min_radius])
        
    def _update_radius(self, radius):
        self._figure.update_layout(
            polar = dict(
                radialaxis=dict(range=[0, radius["new"]])
            )
        )
        
    def _update_min_radius(self, radius):
        self._figure.update_traces(
            selector=dict(name="min_rad"),
            r=[radius["new"] for k in range (len(self._df.Ab))]
        )
        
    def _update_font_size(self, size):
        if not self._figure is None:
            self._figure.update_layout(
                polar = dict(
                    angularaxis = dict(
                        tickfont_size=int(size["new"] * 0.7)
                    )
                ),
                legend=dict(font=dict(size=size["new"]))
            )
            
    def _change_color_palette(self, palette):
        if not self._figure is None:
            old = cycle(common._palettes.get(palette["old"]))
            colors = cycle(common._palettes.get(palette["new"]))
            df_col = self._df.melt(id_vars=['Category','Subcategory','Ab', 'Symptom'], value_vars=self._col).copy()
            dic_color = {}
            dic_color_old = {}
            # circular attribution of the colors (at the end of the palette, we go back to the beginning)
            for scale in df_col['variable'].unique() : 
                dic_color[scale] = next(colors)
                dic_color_old[scale] = next(old)
            
            for scale in dic_color.keys() : 
                self._figure.update_traces(
                    selector=dict(
                        name=scale,
                    ), # name in the legend
                    marker=dict( #property of the markers
                        color = dic_color[scale], # color depending on the scale 
                    )
                )
                self._figure.update_traces(
                    selector=dict(
                        marker=dict( # properties of the markers
                            color = 'white', # white circle with color line
                            symbol = "circle",
                            line=dict(
                                color=dic_color_old[scale], # color of the line
                                width=1, # width of the line
                            )
                        )
                    ), # name in the legend
                    marker=dict( #property of the markers
                        line=dict(
                            color=dic_color[scale]
                        )
                    )
                )

    def _reset_options(self, _):
        super()._reset_options(_)
        self._max_radius.value = self._default_max_radius
        self._min_radius.value = self._default_min_radius

    def _init_circle(self):
        df_col = self._df.melt(id_vars=['Category','Subcategory','Ab', 'Symptom'], value_vars=self._col).copy()
        with melt_output:
            clear_output()
            display(df_col.head())
        min_radius = self._min_radius.value

        # dictionnary questionnaire <->  radius of the circles
        dic = {}
        i = self._max_radius.value
        for scale in df_col.variable.unique() : 
            dic[scale] = i
            i-=1

        # dictionnary scale <-> color
        palette = common._palettes.get(self._colorPicker.value)
        colors = cycle(palette) # choice of the palette. More choice in the following documentation : https://plotly.com/python/builtin-colorscales/
        dic_color = {}
        # circular attribution of the colors (at the end of the palette, we go back to the beginning)
        for scale in df_col['variable'].unique() : 
            dic_color[scale] = next(colors)
        ###
        # FIGURE
        ###
        self._figure = go.FigureWidget()
        # transparency plot with all the symptoms to set their order in the plot
        self._figure.add_trace(go.Scatterpolar(
                    r = [0 for k in range(len(self._df.index))], # list of radiuses
                    theta = self._df.Ab, # list of angles
                    mode = 'markers',
                    showlegend = False, # no legend thanks
                opacity = 0.0, # everything transparent !
            ))

        if self._df.shape[0] == self._df['Category'].isnull().sum() : 
            df_col.loc[:,'Category'] = ""

        ### specific symptoms (value == 1)
        df_spe = df_col[df_col.value == 1].copy() # we isolate only the specific symptoms
        for scale in df_spe.variable.unique() : 
            temp = df_spe[df_spe.variable==scale] # dataframe with the data of each scale
            self._figure.add_trace(
                go.Scatterpolar(
                    r = [dic[scale] for k in range(temp.shape[0])], # constant radius corresponding to the dictionnary value
                    theta = temp.Ab, # angle = symptom 
                    mode = 'markers',
                    name = scale, # name in the legend
                    hoverinfo="text", # type of hover. 'text' means that we design it by hand.
                    hovertext= "Scale: "+scale+"<br>"+"Sympt.:"+temp.Symptom + "<br>Specific"+"<br>Category: "+temp.Category, # \n is <br> (html)
                    # if category column in not empty

                    opacity = 1.0,
                    marker=dict( #property of the markers
                        color = dic_color[scale], # color depending on the scale 
                        symbol = "circle", # we want filled circles
                        line=dict( # property of the line of the markers
                            width=0 # we do not want line !
                        )
                    )
                )
            )

        ### component symptoms (=2)
        df_comp = df_col[df_col.value == 2].copy()# we isolate only the compound symptoms
        for scale in df_comp.variable.unique() : 
            temp = df_comp[df_comp.variable==scale] # dataframe with the data of each scale
            self._figure.add_trace(
                go.Scatterpolar(
                    r = [dic[scale] for k in range(temp.shape[0])], # constant radius corresponding to the dictionnary value
                    theta = temp.Ab,  # angle = symptom
                    mode = 'markers',
                    hoverinfo="text",
                    hovertext= "Scale: "+scale+"<br>"+"Sympt.:"+temp.Symptom + "<br>Compound"+"<br>Category: "+temp.Category, # \n is <br> (html)
                    showlegend = False, # no legend
                    marker=dict( # properties of the markers
                        color = 'white', # white circle with color line
                        symbol = "circle",
                        line=dict(
                            color=dic_color[scale], # color of the line
                            width=1, # width of the line
                        )
                    )
                )
            )
            i+=1

        ### white circle in the center
        self._figure.add_trace(go.Scatterpolar(
            r=[min_radius for k in range (len(self._df.Ab))], # radius of the circle = min_radius (set before)
            theta=self._df.Ab, # all angles
            fill='toself',
            name="min_rad",
            fillcolor = "white", # color of the circle
            hoverinfo='none',
            showlegend = False, # no legend
            line=dict(
                    color="white",
                    width=0, # no line
                )
            )
        )

        ### Set options common to all traces with self._figure.update_traces
        self._figure.update_polars(bgcolor='white')
        self._figure.update_layout(
            autosize=True, # to allow or not autosize
            width=self._default_figure_width, # width of the figure
            height=self._default_figure_height, # height of the figure
            paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor= 'rgba(0,0,0,0)',# background color
            polar = dict( #options for the polar plot
                radialaxis = dict(
                    visible = True, # allowing radius lines  
                    color="lightgrey", # color of the lines
                    gridcolor = "lightgrey", # color of the grid
                    linecolor="lightgrey", #color of the lines
                    gridwidth = 1, # step in the grid
                    range=[0, self._max_radius.value+1], # range of the grid
                    dtick=1, # step in the grid
                    showgrid =True, # showing the grid
                    layer="below traces", # put the grid below traces
                    tickfont_color ='rgba(0,0,0,0)'# putting tickfont into white to make them disappear
                ),
                angularaxis = dict(
                    gridcolor = "lightgrey", # color of the angular grid
                    tickfont_size=int(self._default_font_size * 0.7), # font size of labels (ex. "S01")
                    rotation=90, # start position of angular axis 
                    direction="counterclockwise" # changin direction to align with Fried et al. 
                )
            ),
            legend = dict(font = dict(size = self._default_font_size, color = "black")) # size and color of the legend
        )