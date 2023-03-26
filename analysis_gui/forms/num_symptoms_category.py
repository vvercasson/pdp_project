from .form import Form
from .common import *
from . import common

class NumSymCat(Form):
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
        
        with self._output:
            clear_output()
            # number of categories/questionnaire
            if common.df.shape[0] != common.df['Category'].isnull().sum() : 
                common.cat_per_questionnaire = pd.DataFrame(np.zeros((common.df.shape[1]-5,len(common.df.Category.unique()))), index = common.df.iloc[:,4:-1].columns, columns = common.df.sort_values(by="Ab").Category.unique())
                for category in common.df.Category.unique():
                    common.cat_per_questionnaire.loc[:,category] = (common.df[common.df.Category==category].iloc[:,4:-1]>=1).sum(axis = 0)
                display(common.cat_per_questionnaire.T)
                common.cat_per_questionnaire.T.to_excel("table2_categorie_per_questionnaire.xlsx")
            else : 
                print('No category in this dataframe !')
    