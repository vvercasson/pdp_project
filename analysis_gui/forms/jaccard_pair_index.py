from .common import *
from . import common
from .figure_form import Form
from sklearn.metrics import jaccard_score

class JaccardPairIndex(Form):
    def __init__(self, type: str):
        super().__init__(
            output=Output(width="fit-content"),
            layout=Layout(
                width="max-content",
                grid_gap="10px",
                align_items="flex-start",
                overflow="visible"
            )
        )
        self.type = type
        
    def init(self):
        self.children = [self._output]
        
        if common.df.shape[0] != common.df[self.type].isnull().sum() : 
            res = pd.DataFrame(
                np.zeros((len(common.df[self.type].unique()),1)),
                index = common.df.sort_values(by="Ab")[self.type].unique(),
                columns=['Avg. Jaccard Index']
            )
            
            for category in common.df[self.type].unique() : 
                df_category = common.df.drop(common.header+['sum_symptoms'],axis = 1)[common.df[self.type]==category]
                df_category = df_category.iloc[:,(df_category.sum(axis = 0)!=0.0).to_numpy()] # we keep only the questionnaire with at least 1 symptom
                liste_avg = []
                
                for questionnaire1 in df_category.columns : 
                    liste = []
                    
                    for questionnaire2 in df_category.columns : 
                        if questionnaire1!= questionnaire2 :
                            liste.append(jaccard_score(df_category[questionnaire1]>=1, df_category[questionnaire2]>=1))
                            
                    liste_avg.append(np.mean(liste))
                res.loc[category, 'Avg. Jaccard Index'] = np.mean(liste_avg)
                
            with self._output:
                clear_output()
                display(res)
                
            res.to_excel("table5_jaccard_"+ self.type.lower() +"s.xlsx")
        else: 
            with self._output:
                clear_output()
                print("Category is empty")