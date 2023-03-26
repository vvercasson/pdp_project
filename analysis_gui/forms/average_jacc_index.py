from .common import *
from . import common
from .figure_form import Form
import numpy as np

class AverageJaccardIndex(Form):
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
        self.children = [self._output]
        
        common.jaccard = pd.DataFrame(np.zeros((len(common.df.drop(common.header+['sum_symptoms'],axis = 1).columns),1)), index = common.df.drop(common.header+['sum_symptoms'],axis = 1).columns, columns=['Avg. Jaccard Index'])
        for questionnaire in common.df.drop(common.header+['sum_symptoms'], axis=1).columns : 
            common.jaccard.loc[questionnaire, 'Avg. Jaccard Index'] = common.jaccard_table.drop(common.references+[questionnaire], axis = 1).loc[questionnaire, :].mean()
        # display(jaccard)
        # jaccard.to_excel("table4_jaccard_average_questionnaires.xlsx")
        # print("Average Jaccard index (wo references): "+str(np.round(float(jaccard.mean()),5)) +" (sd: "+str(np.round(float(jaccard.std()),4))+ ")" )
        
        with self._output:
            clear_output(wait=True)
            display(common.jaccard)
            