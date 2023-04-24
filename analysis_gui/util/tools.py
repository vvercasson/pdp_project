from io import BytesIO
import pandas as pd
import os

def get_dialog(message, header, headerclass, dialog_type='generic', extrajs=''):
    if (headerclass != 'success' and headerclass != "failure"):
        raise ValueError("headerclass must be either 'success' or 'failure'")
    html = f"""
    <style>
        /* Modal Content/Box */
        #{dialog_type}-dialog {{
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .modal-content {{
            background-color: #fefefe;
            border: 1px solid #888;
            box-shadow: 0 0 8px rgba(0,0,0,0.2);
            display: flex;
            flex-flow: column;
            grid-gap: 1em;
            border-radius: 5px;
            overflow: hidden;
        }}
        
        #{dialog_type}-dialog[open] {{
            opacity: 1;
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            padding: 0 1em 0 1em;
            align-items: center;
            color: #FFFFFF
        }}
        
        .success {{
            background-color: rgb(25,135,184);
        }}
        
        .failure{{
            background-color: rgb(225,0,44);
        }}

        .body {{
            padding: 0 1em 1em 1em;
        }}

        /* The Close Button */
        .close {{
            color: #FFFFFFFF;
            font-size: 28px;
            font-weight: bold;
        }}
        .close:hover,
        .close:focus {{
            color: #DDDDDD;
            text-decoration: none;
            cursor: pointer;
        }}
    </style>

    <dialog id="{dialog_type}-dialog">
        <!-- Modal content -->
        <div class="modal-content">
            <div class="header {headerclass}">
                <h2>{header}</h2>
                <span class="close">&times;</span>
            </div>
            <div class="body">
                <p>{message}</p>
            </div>
        </div>
    </dialog>
    """
    
    js = f'''
    {extrajs}
    const dialog = document.getElementById("{dialog_type}-dialog");
    const close = document.getElementsByClassName("close")[0];
    dialog.showModal();

    function closeDialog() {{
        var e = dialog.closest(".jp-OutputArea");
        if (e !== null) {{
            e.replaceChildren();
        }}
    }}

    // When the user clicks on <span> (x), close the modal
    close.onclick = function() {{
        closeDialog();
    }}

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {{
        if (event.target == dialog) {{
            closeDialog();
        }}
    }}
    '''
    
    return html, js

def save_dataframe(df, extension):
    """
    Saves a dataframe to a BytesIO object.
    """
    file = BytesIO()
    if extension == '':
        raise ValueError("File extension is needed (.xlsx, ...)")
    if extension == 'csv':
        df.to_csv(file)
    elif extension == 'xlsx' or extension == 'xls':
        writer = pd.ExcelWriter('temp.' + extension) # type: ignore
        df.to_excel(writer)
        writer.book.save(file)
        os.remove('temp.' + extension)
    else:
        raise ValueError(f"Unsupported file type: {extension}")
    return file