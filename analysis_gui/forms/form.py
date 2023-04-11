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
        self.df = None
        
    def init(self):
        pass
    
    def update(self):
        pass
    
    def _parse_kwargs(self, *keys, **kwargs):
        args = {}
        if keys:
            for key in keys :
                try:
                    args[key] = deepcopy(kwargs.get(key, None))
                except TypeError:
                    args[key] = copy(kwargs.get(key, None))
        else:
            args = deepcopy(kwargs)
        
        return args
    