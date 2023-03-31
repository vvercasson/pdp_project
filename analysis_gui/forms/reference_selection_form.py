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
        
        self.buttonGenerate.on_click(self.generateFigures)
        
        self.wantReferences.observe(self.on_wantReferences_change, names='value')
    
    def init(self):
        self.checkBoxes = []
        listRef = (ref for ref in list(common.df.columns) if ref not in common.header)
        for ref in listRef:
            newCheckBox = self.createCheckbox(ref, ref in common.references)
            self.checkBoxes.append(newCheckBox)
            
        self._output.clear_output()
        self.children = [
            HBox(
                children=[self.wantReferences],
                layout=Layout(justify_content="flex-start", grid_gap="5px", width="match-content")
            ),
            GridBox(
                children=self.checkBoxes,
                layout=Layout(grid_template_columns="repeat(3, 33%)")
            ),
            HBox(
                children=[self.buttonGenerate],
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
            self.clearReferences()
            self.children = [self.wantReferences, self.buttonGenerate, self._output]
        else:
            self.init()
            
    def clearReferences(self):
        common.references = []
    
    def generateFigures(self, _):
        # Change the references
        selected_options = []
        for i in self.checkBoxes:
            if i.value and not i.description in common.references:
                selected_options.append(i.description)
        common.references.extend(selected_options)
        
        sums = (common.df.drop(common.header,axis = 1)>=1).sum(axis = 0) # sum of the number of symptom by questionnaire
        common.col = list(sums.sort_values(ascending=False).index.to_numpy()) #we create the list of columns
        common.col = header + common.col
        # we apply the order of columns to the dataset
        common.df = common.df.loc[:, common.col]
        self._output.clear_output(wait=True)
        with self._output:
            clear_output()
            display(common.df.head())
        common.df['sum_symptoms'] = (common.df.drop(common.header,axis = 1)>=1).sum(axis = 1)
        common.df.sort_values(by=['sum_symptoms','Ab'], ascending = [False,True], inplace = True)
        with self._output:
            display(common.df.head())
        self.executeNext()