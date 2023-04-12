from .table_form import TableForm
from .common import *

class NumSymptomsUI(TableForm):
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
        
        super().init(**kwargs)
        # Computing sum of symptoms in DataFrame
        sympt_per_questionnaire = pd.DataFrame(np.zeros((self._df.shape[1]-5,3)), index = self._df.iloc[:,4:-1].columns, columns = ['Specific symptoms', 'Compound symptoms', 'Total'])
        sympt_per_questionnaire['Specific symptoms'] = (self._df.iloc[:,4:-1]==1).sum(axis = 0)
        sympt_per_questionnaire['Compound symptoms'] = (self._df.iloc[:,4:-1]==2).sum(axis = 0)
        sympt_per_questionnaire['Total'] = (self._df.iloc[:,4:-1]>=1).sum(axis = 0)
        
        self._generated_frame = sympt_per_questionnaire
        with self._output:
            clear_output()
            display(sympt_per_questionnaire)
        kwargs["sympt_per_questionnaire"] = sympt_per_questionnaire
        self.executeNext(**kwargs)
