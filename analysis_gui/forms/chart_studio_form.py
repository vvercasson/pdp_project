from analysis_gui.forms.form import Form
from .common import *
import chart_studio
from IPython.display import Javascript
from analysis_gui.util.tools import get_dialog
from ipywidgets import ToggleButtons
from requests.auth import HTTPBasicAuth
import requests

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
        # crochet
        self.has_cs_account = ToggleButtons(
            options =['Yes', 'No'],
            value=None,
            description='Do you have a Chart Studio account ?',
            disabled=False,
        )
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
        self.children = [self.has_cs_account]
        self._login_button.on_click(self.setCredentials)
        self._api_key.observe(self._on_api_key_change, names=['value'])
        self._user_name.observe(self._on_username_change, names=['value'])
        self.has_cs_account.observe(self.on_has_account_change, names='value')
        
    # EVENTS 
    def on_has_account_change(self, change):
        if change['new'] == 'No':
            self.children = [self.has_cs_account]
            self.executeNext()
        else:
            self._output.clear_output()
            self.children = [self.has_cs_account, self._sign_in_layout, self._output]
            
    def _on_api_key_change(self, change):
        self._login_button.disabled = (change["new"] == '') or self._user_name.value == ''
        
    def _on_username_change(self, change):
        self._login_button.disabled = (change["new"] == '') or self._api_key.value == ''
    
    def setCredentials(self, _):
        auth = HTTPBasicAuth(self._user_name.value, self._api_key.value)
        headers = {'Plotly-Client-Platform': 'python'}
        res = requests.get("https://api.plotly.com/v2/folders/themes_shared", auth=auth, headers=headers)
        if (res.status_code == 200):
            html, js = get_dialog("You are now logged in to Chart Studio", "Login successful", "success")
            chart_studio.tools.set_credentials_file(username=self._user_name.value, api_key=self._api_key.value)
            with self._output:
                clear_output(wait=True)
                display(HTML(html), Javascript(js))
            self.executeNext()
        else :
            html, js = get_dialog("Failed to connect to your account, check your credentials", "Login failed", "failure")
            with self._output:
                clear_output(wait=True)
                display(HTML(html), Javascript(js))