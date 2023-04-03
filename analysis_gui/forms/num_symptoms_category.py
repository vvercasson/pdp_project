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
        
    def init(self, **kwargs):
        args = self._parse_kwargs("df", "cat_per_questionnaire", **kwargs)
        df = args["df"]
        self.children = [self._output]
        cat_per_questionnaire = None
        with self._output:
            clear_output()
            # number of categories/questionnaire
            if df.shape[0] != df['Category'].isnull().sum() : 
                cat_per_questionnaire = pd.DataFrame(np.zeros((df.shape[1]-5,len(df.Category.unique()))), index = df.iloc[:,4:-1].columns, columns = df.sort_values(by="Ab").Category.unique())
                for category in df.Category.unique():
                    cat_per_questionnaire.loc[:,category] = (df[df.Category==category].iloc[:,4:-1]>=1).sum(axis = 0)
                display(cat_per_questionnaire.T)
                # cat_per_questionnaire.T.to_excel("table2_categorie_per_questionnaire.xlsx")
            else : 
                print('No category in this dataframe !')

        self.executeNext(df=df, cat_per_questionnaire=cat_per_questionnaire)