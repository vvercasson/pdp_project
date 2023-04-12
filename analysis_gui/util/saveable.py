from abc import abstractmethod
from .tools import get_dialog
from ..forms.common import *
from ipywidgets import Tab

class Saveable():
    
    def __init__(self, placeholder="File name (figure_example.pdf)", tooltip="Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']"):
        Saveable._create_save_interface(self, placeholder, tooltip)
        self._fileName.observe(self._onFileNameChange, names=['value'])
        self._save_button.on_click(self._save)

    def _create_save_interface(self, placeholder, tooltip):
        self._save_dialog = Output()
        self._loading = Image(value=loading_gif, layout=Layout(width="15px", height="15px", visibility="hidden"))
        
        # Save Figure Option
        self._save_button = Button(
            description="Save",
            icon="download",
            tooltip="Click here to save the figure",
            disabled=True,
        )
        self._fileName = Text(
            placeholder=placeholder,
            disabled=False,
            tooltip=tooltip
        )
        
        save_widget = HBox(
            children=[self._fileName, self._save_button, self._loading, self._save_dialog],
            layout=Layout(
                width="match-content",
                justify_content="flex-start",
                align_items="center",
                grid_gap="10px"
            )
        )
        
        self._save_interface = Tab(
            children=[save_widget],
            layout=Layout(
                justify_content="flex-start",
                width="auto"
            )
        )
        
        self._save_interface.set_title(0, "Download")
        
    def _onFileNameChange(self, change):
        if change['new'] == '':
            self._save_button.disabled = True
        else:
            self._save_button.disabled = False
    
    @abstractmethod
    def _save(self, _):
        pass
    
    def _show_interface(self, other=[]):
        self._fileName.value = ''
        self.children = other + [self._save_interface]
    
    def _get_save_dialog(self, message, header, headerclass, filename='', uri=''):
        
        anchor = ''
        if uri != '':
            anchor = f'''
            const a = document.createElement('a');
            a.setAttribute('href', '{uri}');
            a.setAttribute('download', '{filename}')
            a.click();
            '''
        
        return get_dialog(message, header, headerclass, dialog_type='save', extrajs=anchor)