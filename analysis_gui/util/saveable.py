from .tools import get_dialog

class Saveable():

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
        
        return get_dialog(message, header, headerclass, dialog_type='save', extrajs=anchor)