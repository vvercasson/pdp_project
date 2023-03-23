from .common import *
from .form import Form
from ..forms import common

class FileSelectionForm(Form):
    TYPE_XSL = "application/vnd.ms-excel"
    TYPE_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    def __init__(self): 
        super().__init__(
            output=Output(width="fit-content"),
            layout= Layout(
                width="100%",
                grid_gap="10px"
            )
        )
        
        self.dropdown = Dropdown(
            options=["Fried2017", "Gauld2023_OSAS_content_analysis", "Gauld2023_sleep_content_analysis", "Custom"],
            value="Gauld2023_OSAS_content_analysis",
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
            disabled=False,
        )
        
        self.children = [
                HBox(
                    children=[self.dropdown, self.filepicker],
                    layout=Layout(justify_content="flex-start", grid_gap="5px", width="100%")
                ),
                HBox(
                    children=[self.confirm],
                    layout=Layout(justify_content="flex-start", width="100%")
                ),
                self._output
            ]
        
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
        if len(files) > 0 and (files[0].type == FileSelectionForm.TYPE_XLSX or files[0].type == FileSelectionForm.TYPE_XSL):
            # print(files[0].type)
            self.confirm.disabled = False
    
    def confirmForm(self, _):
        common.experiment = self.dropdown.value
        
        if common.experiment == "Fried2017" : 
            common.df = pd.read_excel("./data/fried2017_reformatted.xlsx") # reproduction of the seminal paper of Fried et al. https://doi.org/10.1016/j.jad.2016.10.019
            common.references = []
        elif common.experiment=="Gauld2023_sleep_content_analysis" : 
            common.df = pd.read_excel("./data/gauld2023_sleep_content_analysis_processed.xlsx")
            common.references = ['ICSD', 'DSM']
        elif common.experiment=="Gauld2023_OSAS_content_analysis" : 
            common.df = pd.read_excel("./data/gauld2023_OSAS_data_processed.xlsx")
            common.references = []
        else :
            file = self.filepicker.value[0].content
            common.df = pd.read_excel(io.BytesIO(file))

        common.df.rename(columns={common.df.columns[0]: "Category",common.df.columns[1]: "Subcategory", common.df.columns[2]: "Ab", common.df.columns[3]: "Symptom"}, inplace=True) #replacing the name of the three first columns !
        common.df.sort_values(by="Ab",inplace = True) # sort the dataset by abbreviation
        
        with self._output:
            clear_output()
            display(common.df.head()) # print the 5 first rows
        self.executeNext()