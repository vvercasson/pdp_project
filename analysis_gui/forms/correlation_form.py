from .common import *
from . import common
from .figure_form import Form
from scipy.stats import spearmanr

class Correlation(Form):
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
        args = self._parse_kwargs("jaccard", "sympt_per_questionnaire", **kwargs)
        jaccard, sympt_per_questionnaire = args["jaccard"], args["sympt_per_questionnaire"]
        
        correlations = jaccard.join(sympt_per_questionnaire)
        
        with self._output:
            clear_output()
            display(correlations)
            print("Correlation between Jaccard Index and number of specific symptoms: ",spearmanr(correlations['Avg. Jaccard Index'], correlations['Specific symptoms']))
            print("Correlation between Jaccard Index and number of compound symptoms: ",spearmanr(correlations['Avg. Jaccard Index'], correlations['Compound symptoms']))
            print("Correlation between Jaccard Index and total number of symptoms: ",spearmanr(correlations['Avg. Jaccard Index'], correlations['Total']))