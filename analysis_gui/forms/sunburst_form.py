from analysis_gui.forms.common import *
from analysis_gui.forms import common
from analysis_gui.forms.palette_figure_form import PaletteFigureForm
import textwrap

class SunburstForm(PaletteFigureForm):
    def __init__(self):
        super().__init__(
            default_font_size=11,
            default_figure_width=600,
            default_figure_height=600
        )
        self._options.layout.margin="1em 0 3em 0"
    
    def init(self, **kwargs):
        #replacing some wordings
        args = self._parse_kwargs("df", **kwargs)
        self.df = self.break_columns(args["df"])
        path = []
        if np.sum(self.df.Subcategory.isna()) != self.df.shape[0] : # with category and subcategory
            path = ['Category', 'Subcategory', 'Symptom']
        elif np.sum(self.df.Category.isna()) != self.df.shape[0] : # with category only
            path = ['Category', 'Symptom']
            
        if path:
            fig = px.sunburst(self.df, path=path, values='sum_symptoms', color_discrete_sequence = common._palettes.get(self._colorPicker.value))
            fig.update_layout(margin = dict(t=0, l=0, r=0, b=0), font_size=self._default_font_size, width=self._default_figure_width, height=self._default_figure_height)
            fig.update_traces(insidetextorientation='radial')
            fig.update_traces(hovertemplate='sum_symptom: %{value}')
            
            self._figure=go.FigureWidget(fig)
            self._show_interface()
        else : 
            self.children = [self._output]
            with self._output:
                clear_output()
                print("No category -> no sunburst plot")
        
                
    def break_columns(self, df, max_length = 16):
        categories = []
        subcategories = []
        symptoms = []
        
        if np.sum(df.Category.isna()) != df.shape[0] :
            categories = df.Category.unique().tolist()
        if np.sum(df.Subcategory.isna()) != df.shape[0] :
            subcategories = df.Subcategory.unique().tolist()
        if np.sum(df.Symptom.isna()) != df.shape[0] :
            symptoms = df.Symptom.unique().tolist()
        
        for string in categories + subcategories + symptoms:
            df.replace(string, "<br>".join(textwrap.wrap(string, width=max_length)), inplace = True)
            
        return df.copy()
    
    def _change_color_palette(self, palette):
        categories = self.df.Category.unique()
        # Les tranches du sunburst sont triées par valeur de chaque label
        # donc on est obligés de trier les catégories par ordre décroissant
        # pour leur associer la bonne couleur
        cats = [
            cat for _, cat in sorted(
                zip(self._figure.data[0].values[-len(categories):], self._figure.data[0].labels[-len(categories):]), key=lambda pair: pair[0], reverse=True
            )
        ]
        palette = common._palettes.get(palette["new"])
        c = cycle(palette)
        cols = dict(zip(cats, c))
        
        colors = []
        # Ici on attribue la couleur de la catégorie à chaque tranche du sunburst
        for label in self._figure.data[0].labels:
            # On récupère la catégorie de la tranche
            df = self.df[self.df.isin([label]).any(axis=1)]
            # On attribue la couleur de la catégorie à la tranche
            colors.append(cols[df.Category.unique()[0]])
            
        self._figure.update_traces(marker_colors=colors)
