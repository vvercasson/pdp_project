from .figure_form import FigureForm
from . import common
from .common import *
from ipywidgets import IntSlider

class CircleForm(FigureForm):
    
    def __init__(self):     
        self.intslider = IntSlider(
            value=20,
            min=6,
            max=50,
            step=1,
            description='Max Radius :',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
        
        super().__init__(
            output=Output(width="fit-content"),
            layout= Layout(
                width="max-content",
                grid_gap="10px",
                align_items="flex-start",
                overflow="visible"
            )
        )

    def init(self):
        self._name = "circle"
        self._output = interactive_output(self.update, {'max_radius': self.intslider})
        self._output.layout.width = "fit-content"
        
        children=[
            HBox(
                children=[self.intslider],
                layout=Layout(justify_content="flex-start", grid_gap="5px", width="100%")
            ),
            self._output
        ]
        
        self._show_interface(children)

    def getForm(self):
        return self._layout
    
    def update(self, max_radius):
        df_col = common.df.melt(id_vars=['Category','Subcategory','Ab', 'Symptom'], value_vars=common.col).copy()
        df_col.head()
        min_radius = self.intslider.min

        # dictionnary questionnaire <->  radius of the circles
        dic = {}
        i = max_radius
        for scale in df_col.variable.unique() : 
            dic[scale] = i
            i-=1

        # dictionnary scale <-> color
        palette = px.colors.qualitative.Pastel # choice of the palette. More choice in the following documentation : https://plotly.com/python/builtin-colorscales/
        i = 0
        dic_color = {}
        # circular attribution of the colors (at the end of the palette, we go back to the beginning)
        for scale in df_col['variable'].unique() : 
            if i>len(palette)-1 : 
                i = 0
            dic_color[scale] =palette[i]
            i+=1

        ###
        # FIGURE
        ###

        self._figure = go.Figure()
        # transparency plot with all the symptoms to set their order in the plot
        self._figure.add_trace(go.Scatterpolar(
                    r = [0 for k in range(len(common.df.index))], # list of radiuses
                    theta = common.df.Ab, # list of angles
                    mode = 'markers',
                    showlegend = False, # no legend thanks
                opacity = 0.0, # everything transparent !
            ))

        if common.df.shape[0] == common.df['Category'].isnull().sum() : 
            df_col.loc[:,'Category'] = ""

        ### specific symptoms (value == 1)
        df_spe = df_col[df_col.value == 1].copy() # we isolate only the specific symptoms
        for scale in df_spe.variable.unique() : 
            temp = df_spe[df_spe.variable==scale] # dataframe with the data of each scale
            self._figure.add_trace(go.Scatterpolar(
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
                    ))
            ))

        ### component symptoms (=2)
        df_comp = df_col[df_col.value == 2].copy()# we isolate only the compound symptoms
        for scale in df_comp.variable.unique() : 
            temp = df_comp[df_comp.variable==scale] # dataframe with the data of each scale
            self._figure.add_trace(go.Scatterpolar(
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
                 ))
            ))
            i+=1

        ### white circle in the center
        self._figure.add_trace(go.Scatterpolar(
            r=[min_radius for k in range (len(common.df.Ab))], # radius of the circle = min_radius (set before)
            theta=common.df.Ab, # all angles
            fill='toself',
            fillcolor = "white", # color of the circle
            showlegend = False, # no legend
            line=dict(
            color="white",
            width=0, # no line
                ))
        )


        ### Set options common to all traces with self._figure.update_traces

        self._figure.update_polars(bgcolor='white')
        self._figure.update_layout(
            autosize=True, # to allow or not autosize
            width=600, # width of the figure
            height=500, # height of the figure
            paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor= 'rgba(0,0,0,0)',# background color
            polar = dict( #options for the polar plot
                  radialaxis = dict(visible = True, # allowing radius lines  
                                    color="lightgrey", # color of the lines
                                    gridcolor = "lightgrey", # color of the grid
                                    linecolor="lightgrey", #color of the lines
                                    gridwidth = 1, # step in the grid
                                    range=[0, max_radius+1], # range of the grid
                                    dtick=1, # step in the grid
                                    showgrid =True, # showing the grid
                                    layer="below traces", # put the grid below traces
                                    tickfont_color ='rgba(0,0,0,0)'),# putting tickfont into white to make them disappear
                  angularaxis = dict(
                gridcolor = "lightgrey", # color of the angular grid
                tickfont_size=7, # font size of labels (ex. "S01")
                rotation=90, # start position of angular axis 
                direction="counterclockwise" # changin direction to align with Fried et al. 
                )),
                legend = dict(font = dict(size = 10, color = "black")) # size and color of the legend
        )
        
        self._figure.show() # showing figure