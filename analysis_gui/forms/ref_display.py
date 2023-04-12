from .common import *
from . import common
from .figure_form import Form

class RefDisplayUI(Form):
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
    def init(self, **kwargs):
        args = self._parse_kwargs("df", "references", **kwargs)
        df, references = args["df"], args["references"]
        self.children = [self._output]
        
        with self._output:
            clear_output()
            if len(references) > 0 :
                for ref in references: 
                    print("---", ref, "---")
                    for symptom in df.Symptom.unique() : 
                        if (int(df.loc[df.Symptom == symptom,ref]) == 1 and int(df.loc[df.Symptom == symptom, 'sum_symptoms'])==0) : 
                            print(symptom)
            else : 
                print("References list is empty")