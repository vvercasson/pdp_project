from .common import *
from . import common
from .table_form import TableForm
from sklearn.metrics import jaccard_score

class JaccardTable(TableForm):
    def __init__(self):
        super().__init__(
            layout=Layout(
                grid_gap="20px",
                align_items="flex-start",
                overflow="visible",
                width="max-content"
            )
        )
        
    def init(self, **kwargs):
        super().init(**kwargs)
        
        jaccard_table = pd.DataFrame(np.zeros((self._df.shape[1]-5,self._df.shape[1]-5)), index = self._df.columns[4:-1], columns = self._df.columns[4:-1]) # df.columns[3:-1] : questionnaires without header
        for questionnaire1 in self._df.columns[4:-1] :
            for questionnaire2 in self._df.columns[4:-1] :
                jaccard_table.loc[questionnaire1, questionnaire2] = jaccard_score(self._df[questionnaire1]>=1, self._df[questionnaire2]>=1)
        
        self._generated_frame = jaccard_table
        
        with self._output:
            clear_output()
            display(jaccard_table)
            
        kwargs["jaccard_table"] = jaccard_table
        # print(jaccard_table)
        self.executeNext(**kwargs)