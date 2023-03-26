from .common import *
from . import common
from .figure_form import Form
from sklearn.metrics import jaccard_score

class JaccardPairIndexSub(Form):
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
        
        if common.df.shape[0] != common.df['Subcategory'].isnull().sum(): 
            res = pd.DataFrame(np.zeros((len(common.df.Subcategory.unique()),1)), index = common.df.sort_values(by="Ab").Subcategory.unique(), columns=['Avg. Jaccard Index'])
            for subcategory in common.df.Subcategory.unique() : 
                df_subcategory = common.df.drop(common.header+['sum_symptoms'],axis = 1)[common.df.Subcategory==subcategory]
                df_subcategory = df_subcategory.iloc[:,(df_subcategory.sum(axis = 0)!=0.0).to_numpy()] # we keep only the questionnaire with at least 1 symptom
                liste_avg = []
                for questionnaire1 in df_subcategory.columns : 
                    liste = []
                    for questionnaire2 in df_subcategory.columns : 
                        if questionnaire1!= questionnaire2:
                            liste.append(jaccard_score(df_subcategory[questionnaire1]>=1, df_subcategory[questionnaire2]>=1))
                    liste_avg.append(np.mean(liste))
                res.loc[subcategory, 'Avg. Jaccard Index'] = np.mean(liste_avg)
            with self._output:
                clear_output()
                display(res)
            res.to_excel("table5b_jaccard_subcategories.xlsx")
        else:
            with self._output:
                clear_output() 
                print("Subcategory is empty")