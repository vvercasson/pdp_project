from typing import overload
from .form import Form
from analysis_gui.util.saveable import Saveable
import os, base64
import plotly.io as pio

from IPython.display import Javascript
from .common import *

class FigureForm(Form, Saveable):
    def __init__(self, output, layout):
        super().__init__(output, layout)
        
        self._name = None
        self._figure = None
        self._figure_height = None
        self._figure_width = None
        self._dialog = Output()
        self._dialog.layout.width = '100%'
        with open("resources/loading.gif", 'rb') as img:
            gif = img.read()
        self._loading = Image(value=gif, layout=Layout(width="15px", height="15px", visibility="hidden"))
        self._save_button = Button(
            description="Save",
            icon="save",
            tooltip="Click here to save the figure",
            disabled=True,
        )
        self._fileName = Text(
            # description="File name",
            placeholder="File name (figure_example.pdf)",
            # value="figure_histogram.pdf",
            disabled=False,
            tooltip="Supported formats: ['png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json']"
        )
        
        
        self._save_interface = HBox(
            children=[self._fileName, self._save_button, self._loading, self._dialog],
            layout=Layout(
                width="100%",
                justify_content="flex-start",
                align_items="center",
                grid_gap="10px"
            )
        )
        
        self._save_button.on_click(self._save)
        self._fileName.observe(self._onFileNameChange, names=['value'])

    def _show_interface(self, other):
        self._box__figure_sliderSize = HBox(
            children =[self._figure_height, self._figure_width],
            layout=Layout(justify_content="flex-start", grid_gap="10px", width="100%")
        )
        self._dialog.clear_output()
        self._fileName.value = ''
        self.children = other + [self._box__figure_sliderSize] + [self._figure] + [self._save_interface]
        
    def _onFileNameChange(self, change):
        if change['new'] == '':
            self._save_button.disabled = True
        else:
            self._save_button.disabled = False      
    
    
    def _update_size_height(self, height):
        newHeight = 500 + height.new*2
        self._figure.update_layout(
        autosize=False,
        height=newHeight)
        
    def _update_size_width(self, width):
        newWidth = 500 + width.new*2
        self._figure.update_layout(
        autosize=False,
        width=newWidth)
        
        
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
