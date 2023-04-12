from .common import *
from analysis_gui.forms import common
from .form import Form
from ..util.saveable import Saveable
from ..util.tools import save_dataframe
from IPython.display import clear_output

class TableForm(Form, Saveable):
    
    def __init__(self, output=None, layout=None):
        Form.__init__(self, output, layout)
        Saveable.__init__(self, placeholder="File name (figure_example.xlsx)", tooltip="Supported formats: ['csv', 'xlsx', 'xls']")
        
    def init (self, **kwargs):
        self._show_interface([self._output])
        args = self._parse_kwargs("df", **kwargs)
        df = args["df"]
        self._df = df
        self._generated_frame = None
    
    def _save(self, _):
        filename = self._fileName.value
        if filename == '':
            return
        _, extension = os.path.splitext(filename) # type: ignore
        extension = extension[1:]
        
        file = None
        headerclass = 'failure'
        header = 'Failed'
        mime = ''
        fileuri = ''
        if self._generated_frame is not None:
            self._loading.layout.visibility = 'visible' # type: ignore
            try:
                file = save_dataframe(self._generated_frame, extension)
            except Exception as e:
                message = f'{e}'
            finally:
                self._loading.layout.visibility = "hidden"
                
            if not file is None:
                file = base64.b64encode(file.getbuffer()).decode()
                message = f'Successfully saved image as {filename}'
                headerclass = 'success'
                header = 'Success !'
                mime = common.mime_types[extension]
                fileuri = f"data:{mime};base64,{file}"
        else :
            message = 'No data to save'
        html, js = self._get_save_dialog(message, header, headerclass, filename, fileuri) # type: ignore
        with self._save_dialog:
            clear_output()
            display(HTML(html))
            display(Javascript(js))