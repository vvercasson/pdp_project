from .common import *
from . import common
from .form import Form
from ipywidgets import  Checkbox, GridBox

class HistogramUI(Form):
    
    def __init__(self):
        super().__init__(
            layout=Layout(grid_gap="20px"),
        )
        self._palettes = px.colors.qualitative.__dict__.copy()
        self._df_questionnaires = None
        self._sortBy = "Symptom"
        self._figure = None
        self._dialog = Output()
        with open("resources/loading.gif", 'rb') as img:
            gif = img.read()
        self._loading = Image(value=gif, layout=Layout(width="15px", height="15px", visibility="hidden"))
        self._colorPicker = Dropdown(
            options=[name for name, body 
                     in inspect.getmembers(px.colors.qualitative)
                     if isinstance(body, list) and name != "__all__" and not name.endswith("_r")],
            value='Pastel',
            description="Color Palette",
            disabled=False
        )
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
        
        # self._colorPicker.observe(self._setColorPalette, names=["value"])
        
    def init(self):
        
        self._save.on_click(self._save_figure)
        self._fileName.observe(self._onFileNameChange, names=['value'])
        self._output = interactive_output(self.update, {'palette': self._colorPicker})
        self._output.layout.width = "100%"
        
        self.children = [
            HBox(
                children=[Label(value="PLACEHOLDER"), self._colorPicker],
                layout=Layout(width="100%")
            ),
            HBox(
                children=[self._output],
                layout=Layout(width="95%", justify_content="space-between")
            ),
            HBox(
                children=[self._fileName, self._save, self._loading, self._dialog],
                layout=Layout(
                    width="100%",
                    justify_content="flex-start",
                    align_items="center",
                    grid_gap="10px"
                )
            )
        ]
        if self._df_questionnaires is None:
            self._df_questionnaires = common.df.drop(references, axis = 1).sort_values(by=['sum_symptoms', 'Ab'], ascending=[False,True])

    def update(self, palette, sortBy):
        self._update_figure(palette)
        self._figure.show()
        
    def _update_figure(self, palette):
        if self._figure is None:
            if common.df.shape[0] != common.df['Category'].isnull().sum(): 
                self._color = 'Category'
            else: 
                self._color = 'sum_symptoms'
        colors = self._palettes.get(palette)
        self._figure = px.bar(
            self._df_questionnaires,
            x='Symptom',
            y='sum_symptoms',
            color=self._color,
            labels={'sum_symptoms':'Number of questionnaires'},
            color_discrete_sequence=colors,
            category_orders = {'Category':self._df_questionnaires.sort_values(by='Ab').Category.unique()}
        )
        self._figure.update_layout(xaxis_tickangle=-60,autosize=True, height=600)
        self._figure.update_layout(xaxis={'categoryorder':'array', 'categoryarray': self._df_questionnaires[self._sortBy].unique()})
        
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
            