from .common import *
from . import common
from .figure_form import FigureForm
import numpy as np
from sklearn.metrics import jaccard_score

class JaccardTable(FigureForm):
    def __init__(self):
        super().__init__(
            layout=Layout(
                grid_gap="20px",
                align_items="flex-start",
                overflow="visible",
                width="max-content"
            ),
            output=Output()
        )
        
    def init(self):
        
        self.children = [self._output]
        
        jaccard_table = pd.DataFrame(np.zeros((common.df.shape[1]-5,common.df.shape[1]-5)), index = common.df.columns[4:-1], columns = common.df.columns[4:-1]) # df.columns[3:-1] : questionnaires without header
        for questionnaire1 in common.df.columns[4:-1] : 
            for questionnaire2 in common.df.columns[4:-1] : 
                jaccard_table.loc[questionnaire1, questionnaire2] = jaccard_score(common.df[questionnaire1]>=1, common.df[questionnaire2]>=1)
                
        
        with self._output:
            display(jaccard_table)
            jaccard_table.to_excel("table3_jaccard_pairs.xlsx")