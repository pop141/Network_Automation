import PySimpleGUI as sg
from connect import Connect


def main():
    con = Connect()
    layout = [
        [sg.Text('Save Locaion', size=(15, 1)), sg.InputText(str(con.default_save)), sg.FolderBrowse()],
        [sg.Text('User Name', size=(15, 1)), sg.InputText("", key='Username')],
        [sg.Text('Password', size=(15, 1)), sg.InputText("", key='Password', password_char='*')],
        [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('SSH Backup Tool', layout)
    while True:  # The Event Loop
        event, values = window.read()
        # print(event, values) #to uncomment debug
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Submit':
            con.default_save = values[0]
            try:
                con.connect_ssh(con.default_save, values['Username'], values['Password'])
            except Exception as e:
                sg.popup(e)


if __name__ == '__main__':
    main()
