from analysis_gui.util.saveable import Saveable
from .table_form import TableForm
from .common import *

class NumSymCat(TableForm):
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
        cat_per_questionnaire = None
        with self._output:
            clear_output()
            # number of categories/questionnaire
            if self._df.shape[0] != self._df['Category'].isnull().sum() : 
                cat_per_questionnaire = pd.DataFrame(np.zeros((self._df.shape[1]-5,len(self._df.Category.unique()))), index = self._df.iloc[:,4:-1].columns, columns = self._df.sort_values(by="Ab").Category.unique())
                for category in self._df.Category.unique():
                    cat_per_questionnaire.loc[:,category] = (self._df[self._df.Category==category].iloc[:,4:-1]>=1).sum(axis = 0)
                self._generated_frame = cat_per_questionnaire.T
                display(self._generated_frame)
            else : 
                print('No category in this dataframe !')

        self.executeNext(df=self._df, cat_per_questionnaire=cat_per_questionnaire)