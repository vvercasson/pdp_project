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
        
        
    def init(self):
        # Computing sum of symptoms in DataFrame
        common.sympt_per_questionnaire = pd.DataFrame(np.zeros((common.df.shape[1]-5,3)), index = common.df.iloc[:,4:-1].columns, columns = ['Specific symptoms', 'Compound symptoms', 'Total'])
        common.sympt_per_questionnaire['Specific symptoms'] = (common.df.iloc[:,4:-1]==1).sum(axis = 0)
        common.sympt_per_questionnaire['Compound symptoms'] = (common.df.iloc[:,4:-1]==2).sum(axis = 0)
        common.sympt_per_questionnaire['Total'] = (common.df.iloc[:,4:-1]>=1).sum(axis = 0)
        common.sympt_per_questionnaire.to_excel("table1_symptomes_per_questionnaire.xlsx")
        
        self.children = [self._output]
        
        with self._output:
            clear_output()
            display(common.sympt_per_questionnaire)
