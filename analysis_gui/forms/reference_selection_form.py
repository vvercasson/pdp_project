from .common import *
from . import common
from .form import Form
from ipywidgets import Checkbox, GridBox

class ReferenceSelectionForm(Form):
    
    def __init__(self):
        Form.__init__(
            self,
            layout=Layout(
                width="max-content",
                grid_gap="10px",
                align_items="flex-start",
                overflow="visible"
            )
        )
        
        self.buttonGenerate = Button(
            description="Generate",
            icon="play-circle",
            tooltip="Generate with the above references",
            disabled=False
        )
        self.buttonGenerate.on_click(self.generateFigures)
        
        # Ne fait rien ?
        # with self.output:
        #     display(self.tab)
    
    def init(self):
        self.checkBoxes = []
        
        listRef = (ref for ref in list(common.df.columns) if ref not in common.header)
        for ref in listRef:
            print(ref in common.references)
            newCheckBox = self.createCheckbox(ref, ref in common.references)
            self.checkBoxes.append(newCheckBox)

        self.children = [
            GridBox(
                self.checkBoxes, layout=Layout(grid_template_columns="repeat(3, 33%)")
            ),
            HBox(
                children=[self.buttonGenerate],
                layout=Layout(justify_content="flex-start", grid_gap="5px", width="100%")

            )
        ]
    
    def createCheckbox(self, ref, _value):
        return Checkbox(
            value=_value,
            description=ref,
            disabled=False
        )
    
    def generateFigures(self, _):
        selected_options = []
        for i in self.checkBoxes:
            if(i.value == True):
                selected_options.append(i.description)
        common.header = selected_options
        print(common.header)