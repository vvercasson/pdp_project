from .form import Form
from .common import *
from analysis_gui.util.exportable import Exportable

class FigureForm(Form, Exportable):
    
    def __init__(self, output=None, layout=None, default_font_size=12, default_figure_width=500, default_figure_height=500):
        Form.__init__(self, output, layout)
        Exportable.__init__(self)
    
        self._default_font_size = default_font_size
        self._default_figure_width =default_figure_width
        self._default_figure_height = default_figure_height
        
        self._figure = None
        self._create_options()
        
        self._set_event_handlers()
        
    def _create_options(self):
        # Figure Size Options and Reset Option
        self._figure_height = IntSlider(
            value=self._default_figure_height,
            min=300,
            max=1280,
            step=1,
            description='Height :',
            disabled=False,
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )  
        self._figure_width = IntSlider(
            value=self._default_figure_width,
            min=300,
            max=1280,
            step=1,
            description='Width :',
            disabled=False,
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
        self._font_size = IntSlider(
            value=self._default_font_size,
            min=5,
            max=32,
            step=1,
            description='Font size :',
            disabled=False,
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format='d'
        )
        
        self._reset_button = Button(
            description="Reset",
            icon="undo",
            tooltip="Reset values to default",
            disabled=False
        )
        
        self._options = HBox(
            children=[self._figure_height, self._figure_width, self._font_size, self._reset_button],
            layout=Layout(justify_content="flex-start", grid_gap="10px", width="100%")
        )
        
    def _set_event_handlers(self):
        self._reset_button.on_click(self._reset_options)
        self._figure_width.observe(self._update_size_width, names=["value"]) # type: ignore
        self._figure_height.observe(self._update_size_height, names=["value"]) # type: ignore
        self._font_size.observe(self._update_font_size, names=["value"]) # type: ignore

    def _show_interface(self, other=[]):
        self._save_dialog.clear_output()            
        Exportable._show_interface(self, other + [self._options] + [self._figure])
    
    def _update_size_height(self, height):
        self._update_size(height=height.new)
        
    def _update_size_width(self, width):
        self._update_size(width=width.new)
        
    def _update_size(self, width=None, height=None):
        if not self._figure is None:
            if not width is None:
                self._figure.update_layout(
                    width=width
                )
            if not height is None:
                self._figure.update_layout(
                    height=height
                )
    
    def _reset_options(self, _):
        self._figure_width.value = self._default_figure_width
        self._figure_height.value = self._default_figure_height
        self._font_size.value = self._default_font_size
                
    def _update_font_size(self, size):
        if not self._figure is None:
            self._figure.update_layout(
                font=dict(size=size.new)
            )
        
    def _export(self, _):
        self._figure.update_layout(autosize=False) # type: ignore
        super()._export(self._figure)
    
    def _save(self, _):
        if self._figure != None:
            filename = self._fileName.value
            if filename == '':
                return
            
            _, extension = os.path.splitext(filename) # type: ignore
            extension = extension[1:]
            image = None
            headerclass = 'failure'
            header = 'Failed'
            mime = ''
            fileuri = ''
            self._loading.layout.visibility = 'visible' # type: ignore
            try:
                image = self._figure.to_image(extension, width=self._figure.layout.width, height=self._figure.layout.height)
            except Exception as e:
                message = f'{e}'
            finally:
                self._loading.layout.visibility = "hidden" # type: ignore
            if image != None:
                image = base64.b64encode(image).decode()
                message = f'Successfully saved image as {filename}'
                headerclass = 'success'
                header = 'Success !'
                mime = "image" if extension != "pdf" else "application"
                fileuri = f"data:{mime}/{extension};base64,{image}"
            html, js = self._get_save_dialog(message, header, headerclass, filename, fileuri) # type: ignore
            with self._save_dialog:
                clear_output(wait=True)
                display(HTML(html), Javascript(js))
