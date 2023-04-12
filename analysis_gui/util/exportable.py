from .tools import get_dialog
from ..forms.common import *
from .saveable import Saveable
import chart_studio as cs
import chart_studio.plotly as py
from chart_studio.exceptions import PlotlyRequestError

class Exportable(Saveable):
    
    def __init__(self):
        super().__init__()
        Exportable._create_save_interface(self)
        Exportable._set_event_handlers(self)  
    
    def _create_save_interface(self):
        self._export_dialog = Output()
        # ChartStudio Export Option
        self._exportCSbutton = Button(
            description="Export to Chart Studio",
            tooltip="Export the figure to Chart Studio",
            icon="cloud-upload",
            disabled=True,
            layout=Layout(width="max-content")
        )
        self._CSfilename = Text(
            placeholder="Chart Studio figure name",
            disabled=False,
            tooltip="The name of the figure in Chart Studio"
        )
        self._export_widget = HBox(
            children=[self._CSfilename, self._exportCSbutton, self._export_dialog, self._loading],
            layout=Layout(
                width="fit-content",
                justify_content="flex-start",
                align_items="center",
                grid_gap="10px"
            )
        )
        
    def _set_event_handlers(self):
        # Events
        self._CSfilename.observe(self._on_cs_file_name_change, names=['value']) # type: ignore
        self._exportCSbutton.on_click(self._export)
    
    def _add_export(self):
        self._save_interface.children = [self._save_interface.children[0], self._export_widget] # type: ignore
        self._save_interface.set_title(1, "Export")
    
    def _export(self, to_export):
        header = "Export Failed"
        headerclass = "failure"
        self._loading.layout.visibility = "visible"
        try:
            url = py.plot(to_export, filename=self._CSfilename.value, auto_open=True, sharing='public')
            message = f"Successfully exported to Chart Studio, link : <a href=\"{url}\" target=\"_blank\">{url}</a>"
            header = "Export Successful"
            headerclass = "success"
        except PlotlyRequestError as e:
            message = f"Export to Chart Studio failed, error: {e}"
        finally:
            self._loading.layout.visibility = "hidden"
        html,js = get_dialog(message, header, headerclass)
        with self._export_dialog:
            clear_output()
            display(HTML(html), Javascript(js))
    
    def _show_interface(self, other=[]):
        self._CSfilename.value = ''
        if cs.tools.get_credentials_file().get("api_key"):
            self._add_export()
        super()._show_interface(other)
    
    def _get_export_dialog(self, message, header, headerclass, dialog_type='export', extrajs=''):
        return get_dialog(message, header, headerclass, dialog_type, extrajs)

    def _on_cs_file_name_change(self, change):
        if change['new'] == '':
            self._exportCSbutton.disabled = True
        else:
            self._exportCSbutton.disabled = False
