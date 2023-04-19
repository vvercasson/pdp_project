from .common import *
from . import common
from .form import Form
from ipywidgets import Checkbox, GridBox, ToggleButtons

class ReferenceSelectionForm(Form):
    
    def __init__(self):
        super().__init__(
            output=Output(width="fit-content"),
            layout=Layout(
                width="max-content",
                grid_gap="10px",
                align_items="flex-start",
                overflow="visible"
            )
        )
        
        self.wantReferences = ToggleButtons(
            options =['Yes', 'No'],
            value=None,
            description='Do you want to select references?',
            disabled=False,
            tooltips=['Yes I want to use references', 'No I don\'t want to specify any references'],
        )
        
        self.buttonGenerate = Button(
            description="Generate",
            icon="play-circle",
            tooltip="Generate with the above references",
            disabled=False
        )
        
        self._boxes_grid = GridBox(
            layout=Layout(grid_template_columns="repeat(3, 33%)")
        )
        
        self._loading = Image(value=loading_gif, layout=Layout(width="1.5em", height="1.5em", visibility="hidden"))
        
        self.buttonGenerate.on_click(self.generateFigures)
        self.wantReferences.observe(self.on_wantReferences_change, names='value')
    
    def init(self, **kwargs):
        args = self._parse_kwargs("df", "references", **kwargs)
        self.df = args["df"]
        self.references = args["references"]
        self.checkBoxes = []
        listRef = (ref for ref in list(self.df.columns) if ref not in common.header)
        for ref in listRef:
            newCheckBox = self.createCheckbox(ref, ref in self.references)
            self.checkBoxes.append(newCheckBox)
        self._boxes_grid.children = self.checkBoxes
        self._output.clear_output()
        self.children = [
            HBox(
                children=[self.wantReferences],
                layout=Layout(justify_content="flex-start", grid_gap="5px", width="match-content")
            ),
            HBox(
                children=[self.buttonGenerate, self._loading],
                layout=Layout(justify_content="flex-start", grid_gap="5px", width="100%")
            ),
            self._output
        ]
    
    def createCheckbox(self, ref, _value):
        return Checkbox(
            value=_value,
            description=ref,
            disabled=False
        )
    
    def on_wantReferences_change(self, change):
        if change['new'] == 'No':
            self.children = [self.wantReferences, self.buttonGenerate, self._output]
        else:
            self._output.clear_output()
            self.children = [self.wantReferences, self._boxes_grid, self.buttonGenerate, self._output]
            
    def generateFigures(self, _):
        # Change the references
        selected_options = []
        for i in self.checkBoxes:
            if i.value and not i.description in self.references:
                selected_options.append(i.description)
    
        sums = (self.df.drop(common.header,axis = 1)>=1).sum(axis = 0) # sum of the number of symptom by questionnaire
        col = list(sums.sort_values(ascending=False).index.to_numpy()) #we create the list of columns
        col = common.header + col
        
        # we apply the order of columns to the dataset
        df = self.df.loc[:, col]
        df['sum_symptoms'] = (df.drop(common.header, axis = 1)>=1).sum(axis = 1)
        df.sort_values(by=['sum_symptoms','Ab'], ascending = [False,True], inplace = True)
        
        with self._output:
            clear_output(wait=True)
            display(df)
            
        self._loading.layout.visibility = "visible"
        self.executeNext(df=df, references=self.references + selected_options, col=col)
        self._loading.layout.visibility = "hidden"
        