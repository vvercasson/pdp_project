from .form import Form
from .common import *
from . import common

class NumSymptomsUI(Form):
    
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
        
        args = self._parse_kwargs("df", **kwargs)
        df = args["df"]
        # Computing sum of symptoms in DataFrame
        sympt_per_questionnaire = pd.DataFrame(np.zeros((df.shape[1]-5,3)), index = df.iloc[:,4:-1].columns, columns = ['Specific symptoms', 'Compound symptoms', 'Total'])
        sympt_per_questionnaire['Specific symptoms'] = (df.iloc[:,4:-1]==1).sum(axis = 0)
        sympt_per_questionnaire['Compound symptoms'] = (df.iloc[:,4:-1]==2).sum(axis = 0)
        sympt_per_questionnaire['Total'] = (df.iloc[:,4:-1]>=1).sum(axis = 0)
        
        self.children = [self._output]
        
        with self._output:
            clear_output()
            display(sympt_per_questionnaire)
        kwargs["sympt_per_questionnaire"] = sympt_per_questionnaire
        self.executeNext(**kwargs)
