from .common import *
from . import common
from .figure_form import Form

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
        
    def init(self, **kwargs):
        self.children = [self._output]
        args = self._parse_kwargs("df", "jaccard_table", "references", **kwargs)
        df, jaccard_table, references = args["df"], args["jaccard_table"], args["references"]
        
        jaccard = pd.DataFrame(np.zeros((len(df.drop(header+['sum_symptoms'],axis = 1).columns),1)), index = df.drop(header+['sum_symptoms'],axis = 1).columns, columns=['Avg. Jaccard Index'])
        for questionnaire in df.drop(header+['sum_symptoms'], axis=1).columns : 
            jaccard.loc[questionnaire, 'Avg. Jaccard Index'] = jaccard_table.drop(references+[questionnaire], axis = 1).loc[questionnaire, :].mean()
        # display(jaccard)
        # jaccard.to_excel("table4_jaccard_average_questionnaires.xlsx")
        # print("Average Jaccard index (wo references): "+str(np.round(float(jaccard.mean()),5)) +" (sd: "+str(np.round(float(jaccard.std()),4))+ ")" )
        
        with self._output:
            clear_output(wait=True)
            display(jaccard)
            
        kwargs["jaccard"] = jaccard
        self.executeNext(**kwargs)
            