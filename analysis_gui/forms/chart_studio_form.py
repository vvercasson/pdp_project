from analysis_gui.forms.form import Form
from .common import *
from . import common
import chart_studio

class ChartStudioForm(Form):
    def __init__(self):
        super().__init__(
            output=Output(width="fit-content"),
            layout=Layout(
                width="max-content",
                grid_gap="10px",
                align_items="flex-start",
                overflow="visible"
            )
        )
        self._createLoginLayout()
    
    def _createLoginLayout(self):
        # ChartStudio Sign in Widgets   
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
        
        # Layout with everything
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
        self.children = [self._sign_in_layout]
        self._login_button.on_click(self.setCredentials)
        self._api_key.observe(self._on_api_key_change, names=['value'])
        self._user_name.observe(self._on_username_change, names=['value'])
        
    # EVENTS 
    # def _on_cs_file_name_change(self, change):
    #     self._login_button.disabled = (change["new"] == '') or self._api_key.value == '' 
            
    def _on_api_key_change(self, change):
        self._login_button.disabled = (change["new"] == '') or self._user_name.value == ''
        
    def _on_username_change(self, change):
        self._login_button.disabled = (change["new"] == '') or self._api_key.value == ''
    
    def setCredentials(self, _):
        chart_studio.tools.set_credentials_file(username=self._user_name.value, api_key=self._api_key.value)
        
        
        
    def init(self, **kwargs):
        with self._output:
            display(self._sign_in_layout)