from .form import Form
import os, base64
import plotly.io as pio
from ipywidgets import HTML

from IPython.display import Javascript
from .common import *

class FigureForm(Form):
    
    def __init__(self, output, layout):
        super().__init__(output, layout)
        
        self._figure = None
        self._dialog = Output()
        with open("resources/loading.gif", 'rb') as img:
            gif = img.read()
        self._loading = Image(value=gif, layout=Layout(width="15px", height="15px", visibility="hidden"))
        
        self._save = Button(
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
            children=[self._fileName, self._save, self._loading, self._dialog],
            layout=Layout(
                width="100%",
                justify_content="flex-start",
                align_items="center",
                grid_gap="10px"
            )
        )
        
    def _show_interface(self, children):
        
        self._save.on_click(self._save_figure)
        self._fileName.observe(self._onFileNameChange, names=['value'])
        
        self.children = children + [self._save_interface]
        
    def _onFileNameChange(self, change):
        if change['new'] == '':
            self._save.disabled = True
        else:
            self._save.disabled = False      
    
    def _save_figure(self, _):
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
                image = pio.to_image(self._figure, extension, width=1440, height=600)
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
            self._display_dialog(message, header, headerclass, filename, fileuri)
            
    def _display_dialog(self, message, header, headerclass, filename='', uri=''):
        html = f"""
        <style>
            /* Modal Content/Box */
            #saveSuccess {{
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            .modal-content {{
                background-color: #fefefe;
                border: 1px solid #888;
                box-shadow: 0 0 8px rgba(0,0,0,0.2);
                display: flex;
                flex-flow: column;
                grid-gap: 1em;
                border-radius: 5px;
                overflow: hidden;
            }}
            
            #saveSuccess[open] {{
                opacity: 1;
            }}

            .header {{
                display: flex;
                justify-content: space-between;
                padding: 0 1em 0 1em;
                align-items: center;
                color: #FFFFFF
            }}
            
            .success {{
                background-color: rgb(25,135,184);
            }}
            
            .failure{{
                background-color: rgb(225,0,44);
            }}

            .body {{
                padding: 0 1em 1em 1em;
            }}

            /* The Close Button */
            .close {{
                color: #FFFFFFFF;
                font-size: 28px;
                font-weight: bold;
            }}
            .close:hover,
            .close:focus {{
                color: #DDDDDD;
                text-decoration: none;
                cursor: pointer;
            }}
        </style>

        <dialog id="saveSuccess">
            <!-- Modal content -->
            <div class="modal-content">
                <div class="header {headerclass}">
                    <h2>{header}</h2>
                    <span class="close">&times;</span>
                </div>
                <div class="body">
                    <p>{message}</p>
                </div>
            </div>
        </dialog>
        """
        
        anchor = ''
        if uri != '':
            anchor = f'''
            const a = document.createElement('a');
            a.setAttribute('href', '{uri}');
            a.setAttribute('download', '{filename}')
            a.click();
            '''
        js = f'''
        const dialog = document.getElementById("saveSuccess");
        const close = document.getElementsByClassName("close")[0];
        dialog.showModal();

        function closeDialog() {{
            dialog.close();
            var e = dialog.closest(".jp-OutputArea");
            if (e !== null) {{
                e.replaceChildren();
            }}
        }}

        // When the user clicks on <span> (x), close the modal
        close.onclick = function() {{
            closeDialog();
        }}

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {{
            if (event.target == dialog) {{
                closeDialog();
            }}
        }}
        '''
        with self._dialog:
            display(HTML(html), Javascript(anchor + js))
