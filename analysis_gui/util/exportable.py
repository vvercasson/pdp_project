from .tools import get_dialog

class Exportable():
    
    def _export(self, _):
        pass
    
    def _get_export_dialog(self, message, header, headerclass, dialog_type='export', extrajs=''):
        return get_dialog(message, header, headerclass, dialog_type, extrajs)