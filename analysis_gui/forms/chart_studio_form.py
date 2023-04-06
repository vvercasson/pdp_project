from analysis_gui.forms.form import Form
from .common import *
import chart_studio
from IPython.display import Javascript
from analysis_gui.util.tools import get_dialog
from ipywidgets import ToggleButtons

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
        self.hasCSAccount = ToggleButtons(
            options =['Yes', 'No'],
            value='No',
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
        self.children = [self.hasCSAccount]
        self._login_button.on_click(self.setCredentials)
        self._api_key.observe(self._on_api_key_change, names=['value'])
        self._user_name.observe(self._on_username_change, names=['value'])
        self.hasCSAccount.observe(self.on_hasAccount_change, names='value')
        
    # EVENTS 
    def on_hasAccount_change(self, change):
        if change['new'] == 'No':
            self.children = [self.hasCSAccount]
        else:
            self._output.clear_output()
            self.children = [self.hasCSAccount, self._sign_in_layout, self._output]
            
    def _on_api_key_change(self, change):
        self._login_button.disabled = (change["new"] == '') or self._user_name.value == ''
        
    def _on_username_change(self, change):
        self._login_button.disabled = (change["new"] == '') or self._api_key.value == ''
    
    def setCredentials(self, _):
        chart_studio.tools.set_credentials_file(username=self._user_name.value, api_key=self._api_key.value)
        html, js = get_dialog("You are now logged in to Chart Studio", "Success", "success", "login")
        with self._output:
            display(HTML(html), Javascript(js))