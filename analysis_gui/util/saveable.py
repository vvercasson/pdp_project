from analysis_gui.util.exportable import Exportable

class Saveable(Exportable):

    def _save(self, _):
        pass
    
    def _get_save_dialog(self, message, header, headerclass, filename='', uri=''):
        
        anchor = ''
        if uri != '':
            anchor = f'''
            const a = document.createElement('a');
            a.setAttribute('href', '{uri}');
            a.setAttribute('download', '{filename}')
            a.click();
            '''
        
        return self._get_export_dialog(message, header, headerclass, dialog_type='save', extrajs=anchor)