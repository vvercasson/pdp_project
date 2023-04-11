import os, base64

from .form import Form
from .common import *
from analysis_gui.util.saveable import Saveable

from IPython.display import Javascript
from ipywidgets import Tab

import chart_studio as cs
import chart_studio.plotly as py
from chart_studio.exceptions import PlotlyRequestError

class FigureForm(Form, Saveable):
    
    def __init__(self, output, layout, default_font_size=12, default_figure_width=500, default_figure_height=500):
        super().__init__(output, layout)
        
        self._default_font_size = default_font_size
        self._default_figure_width =default_figure_width
        self._default_figure_height = default_figure_height
        
        self._figure = None
        self._dialog = Output()
        self._dialog.layout.width = '100%'
        with open("resources/loading.gif", 'rb') as img:
            gif = img.read()
        self._loading = Image(value=gif, layout=Layout(width="15px", height="15px", visibility="hidden"))
        
        self._create_save_interface()
        self._create_options()
        
        self._set_event_handlers()
        
    def _create_save_interface(self):        
        # Save Figure Option
        self._save_button = Button(
            description="Save",
            icon="download",
            tooltip="Click here to save the figure",
            disabled=True,
        )
        self._fileName = Text(
            placeholder="File name (figure_example.pdf)",
            disabled=False,
            tooltip="Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']"
        )
        
        save_widget = HBox(
            children=[self._fileName, self._save_button, self._loading, self._dialog],
            layout=Layout(
                width="match-content",
                justify_content="flex-start",
                align_items="center",
                grid_gap="10px"
            )
        )
        
        # ChartStudio Export Option
        self._exportCSbutton = Button(
            description="Export to Chart Studio",
            tooltip="Export the figure to Chart Studio",
            icon="cloud-upload",
            disabled=True
        )
        
        self._CSfilename = Text(
            placeholder="Chart Studio figure name",
            disabled=False,
            tooltip="The name of the figure in Chart Studio"
        )
        
        self._user_name = Text(
            placeholder="Chart Studio username/email",
            disabled=False,
            tooltip="Your Chart Studio username or email"
        )
        self._api_key = Text(
            placeholder="Chart Studio API key",
            disabled=False,
            tooltip="The API key of your Chart Studio account"
        )
        self._login_button = Button(
            description="Login",
            tooltip="Login to Chart Studio",
            disabled=True,
            icon="sign-in"
        )
            
        export = HBox(
            children=[self._CSfilename, self._exportCSbutton, self._loading],
            layout=Layout(
                width="fit-content",
                justify_content="flex-start",
                align_items="center",
                grid_gap="10px"
            )
        )
        
        self._export_widget = VBox(
            children=[export],
            layout=Layout(
                grid_gap="10px",
            )
        )
        
        self._sign_in_layout = TwoByTwoLayout(
            top_left=self._user_name,
            bottom_left=self._api_key,
            top_right=self._login_button,
            merge=False,
            layout=Layout(
                width="fit-content",
                grid_gap="5px 20px"
            )
        )
        
        self._save_interface = Tab(
            children=[save_widget],
            layout=Layout(
                justify_content="flex-start"
            )
        )
        
        self._save_interface.set_title(0, "Download")
        
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
        # Events
        self._CSfilename.observe(self._on_cs_file_name_change, names=['value'])
        self._api_key.observe(self._on_api_key_change, names=['value'])
        self._save_button.on_click(self._save)
        self._exportCSbutton.on_click(self._export)
        self._reset_button.on_click(self._reset_options)
        self._fileName.observe(self._onFileNameChange, names=['value'])
        self._figure_width.observe(self._update_size_width, names=["value"])
        self._figure_height.observe(self._update_size_height, names=["value"])
        self._font_size.observe(self._update_font_size, names=["value"])


    def _on_cs_file_name_change(self, change):
        if change['new'] == '':
            self._exportCSbutton.disabled = True
        else:
            self._exportCSbutton.disabled = False
            
    def _on_api_key_change(self, change):
        if change['new'] == '':
            self._exportCSbutton.disabled = True
        else:
            self._exportCSbutton.disabled = False

    def _add_sign_in(self):
        self._save_interface.children = [self._save_interface.children[0], self._export_widget]
        self._save_interface.set_title(1, "Export")

    def _show_interface(self, other=[]):
        self._dialog.clear_output()
        self._CSfilename.value = ''
        self._fileName.value = ''
        if cs.tools.get_credentials_file().get("api_key"):
            self._add_sign_in()
        self.children = other + [self._options] + [self._figure] + [self._save_interface]
        
    def _onFileNameChange(self, change):
        if change['new'] == '':
            self._save_button.disabled = True
        else:
            self._save_button.disabled = False
    
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
            
    def _login_chart_studio(self, _):
        cs.tools.set_credentials_file(username=self._cs_username.value, api_key=self._api_key.value)
        self._exportCSbutton.disabled = False
        
    def _export(self, _):
        # self._figure.update_layout(autosize=False)
        try:
            py.plot(self._figure, filename=self._CSfilename.value, auto_open=True, sharing='public')
        except PlotlyRequestError as e:
            pass
        
        # py.plot()
    
    def _save(self, _):
        # print("being called by ", inspect.stack())
        if self._figure != None:
            filename = self._fileName.value
            if filename == '':
                return
            _, extension = os.path.splitext(filename)
            extension = extension[1:]
            image = None
            headerclass = 'failure'
            header = 'Failed'
            mime = ''
            fileuri = ''
            self._loading.layout.visibility = 'visible'
            try:
                image = self._figure.to_image(extension, width=self._figure.layout.width, height=self._figure.layout.height)
            except Exception as e:
                message = f'{e}'
            finally:
                self._loading.layout.visibility = "hidden"
            if image != None:
                image = base64.b64encode(image).decode()
                message = f'Successfully saved image as {filename}'
                headerclass = 'success'
                header = 'Success !'
                mime = "image" if extension != "pdf" else "application"
                fileuri = f"data:{mime}/{extension};base64,{image}"
            html, js = self._get_save_dialog(message, header, headerclass, filename, fileuri)
            with self._dialog:
                display(HTML(html), Javascript(js))
