from .common import *
from . import common
from .figure_form import FigureForm
from sklearn.metrics import jaccard_score

class JaccardTable(FigureForm):
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
        self.children = [self._output]
        
        args = self._parse_kwargs("df", **kwargs)
        df = args["df"]
        
        jaccard_table = pd.DataFrame(np.zeros((df.shape[1]-5,df.shape[1]-5)), index = df.columns[4:-1], columns = df.columns[4:-1]) # df.columns[3:-1] : questionnaires without header
        for questionnaire1 in df.columns[4:-1] :
            for questionnaire2 in df.columns[4:-1] :
                jaccard_table.loc[questionnaire1, questionnaire2] = jaccard_score(df[questionnaire1]>=1, df[questionnaire2]>=1)
    
        with self._output:
            clear_output()
            display(jaccard_table)
            # jaccard_table.to_excel("table3_jaccard_pairs.xlsx")
        kwargs["jaccard_table"] = jaccard_table
        self.executeNext(**kwargs)