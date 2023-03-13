from ipywidgets import Layout, FileUpload, Button, Box, VBox, HBox, Dropdown, Output, interactive_output

class FileSelectionForm(VBox):
    def __init__(self):     
        self.dropdown = Dropdown(
            options=["Fried2017", "GauldMartin2022", "Custom"],
            value="GauldMartin2022",
            description="Expérience",
            disabled=False
        )
        self.filepicker = FileUpload(
            accept=".xsl, .xlsx",
            multiple=False,
            tooltip="Upload your excel file",
            layout=Layout(display='none'),
            disabled=False
        )
        self.confirm = Button(
            description="Confirm",
            icon="check",
            tooltip="Click here to confirm your selection",
            disabled=False
        )
        self.output = Output(
            layout=Layout(
                width="fit-content"
            )
        )
        
        VBox.__init__(
            self,
            children=[
                HBox(
                    children=[self.dropdown, self.filepicker],
                    layout=Layout(justify_content="flex-start", grid_gap="5px", width="100%")
                ),
                HBox(
                    children=[self.confirm],
                    layout=Layout(justify_content="flex-start", width="100%")
                ),
                self.output
            ],
            layout= Layout(
                width="max-content",
                grid_gap="10px",
                align_items="flex-start",
                overflow="visible"
            )
        )
        
        self.dropdown.observe(self._onDropdownChange, names="value")
        self.filepicker.observe(self._onFileUpload, names="value")
        self.confirm.on_click(self.confirmForm)
        
    def _onDropdownChange(self, change):
        if change["new"] == "Custom":
            self.filepicker.layout.display = ""
            if len(self.filepicker.value) == 0:
                self.confirm.disabled = True
        else :
            self.filepicker.layout.display = "none"
            self.confirm.disabled = False
            
    def _onFileUpload(self, change):
        files = change["new"]
        if len(files) > 0 and (files[0].type == TYPE_XLSX or files[0].type == TYPE_XSL):
            print(files[0].type)
            self.confirm.disabled = False
    
    def getForm(self):
        return self._layout
    
    def confirmForm(self, _):
        global df, experiment 
        experiment = self.dropdown.value
        if experiment == "Fried2017" : 
            df = pd.read_excel("./data/fried2017_reformatted.xlsx") # reproduction of the seminal paper of Fried et al. https://doi.org/10.1016/j.jad.2016.10.019
        elif experiment=="GauldMartin2022" : 
            df = pd.read_excel("./data/database_symptoms_sleep_content_analysis.xlsx")
        else :
            file = self.filepicker.value[0].content
            df = pd.read_excel(io.BytesIO(file))

        df.rename(columns={df.columns[0]: "Category", df.columns[1]: "Ab", df.columns[2]: "Symptom"}, inplace=True) #replacing the name of the three first columns !
        df.sort_values(by="Ab",inplace = True) # sort the dataset by abbreviation
        with self.output:
            self.output.clear_output()
            display(df.head()) # print the 5 first rows