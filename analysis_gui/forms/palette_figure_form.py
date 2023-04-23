from .common import *
from .figure_form import FigureForm
import analysis_gui.forms.common as common
import time


class PaletteFigureForm(FigureForm):
    
    def __init__(self, output=None, layout=None, default_font_size=12, default_figure_width=500, default_figure_height=500, default_palette="Pastel"):
        super().__init__(output, layout, default_font_size, default_figure_width, default_figure_height)
        self._default_palette = default_palette
        self._colorPicker = Dropdown(
            # options=[name for name, body 
            #          in inspect.getmembers(px.colors.qualitative)
            #          if isinstance(body, list) and name != "__all__" and not name.endswith("_r")],
            options=list(common._palettes.keys()),
            value=default_palette,
            description="Color Palette",
            disabled=False
        )
        self._colorPicker.observe(self._change_color_palette, names=["value"])
        
    def _show_interface(self, other=[]):
        other = HBox(
                children=other + [self._colorPicker],
                layout=Layout(width="100%", grid_gap="10px")
        )
        return super()._show_interface([other])
        
    def _change_color_palette(self, palette):
        # print(self._figure.data)
        colors = cycle(common._palettes.get(palette["new"]))
        for component in self._figure.data:
            component.update(marker={'color' : next(colors)})            
            
    def _reset_options(self, _):
        self._colorPicker.value = self._default_palette
        return super()._reset_options(_)


 