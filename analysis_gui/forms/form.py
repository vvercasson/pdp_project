from .common import *
from analysis_gui.forms import common
from ..util.chainable import Chainable

class Form(VBox, Chainable):
    
    def __init__(self, output=Output(), layout=Layout()):
        VBox.__init__(
            self,
            layout=layout
        )
        Chainable.__init__(self)
        
        self._output = output
        
    def init(self):
        pass
    
    def update(self):
        pass
    