from .common import *
from . import common
from .figure_form import Form

class RefDisplayUI(Form):
    def __init__(self):
        super().__init__(output=Output(width="fit-content"),
                        layout=Layout(
                            width="max-content",
                            grid_gap="10px",
                            align_items="flex-start",
                            overflow="visible"
                            )
                        )
    def init(self):
        self.children = [self._output]
        
        with self._output:
            clear_output()
            if len(common.references) > 0 :
                for ref in common.references: 
                    print("---", ref, "---")
                    for symptom in common.df.Symptom.unique() : 
                        if (int(common.df.loc[common.df.Symptom == symptom,ref]) == 1 and int(common.df.loc[common.df.Symptom == symptom, 'sum_symptoms'])==0) : 
                            print(symptom)
            else : 
                print("References list is empty")