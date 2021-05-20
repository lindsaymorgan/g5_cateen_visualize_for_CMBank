"""
 PySimpleGUI The Complete Course Lesson 7 - Multiple Windows"""
import PySimpleGUI as sg
from getloactionfrombaidu import get_data

# Design pattern 1 - First window does not remain active

layout = [[ sg.Text('Window 1'),],
          [sg.Input()],
          # [sg.Text('', key='_OUTPUT_')],
          [sg.Button('Launch 2')]]

win1 = sg.Window('Window 1', layout)
win2_active=False
while True:
    ev1, vals1 = win1.Read(timeout=100)
    canteen_list= vals1[0].split('，')
    if ev1 == sg.WIN_CLOSED:
        break
    # win1['_OUTPUT_'].update(vals1[0])

    if ev1 == 'Launch 2'  and not win2_active:
        win2_active = True
        win1.Hide()
        layout2 =  [[sg.Checkbox('My first Checkbox!', default=True)],
                    [sg.Checkbox('My second Checkbox!')],
                    [sg.Submit(), sg.Cancel()]                   ]
     # note must create a layout from scratch every time. No reuse


        win2 = sg.Window('Window 2', layout2)
        while True:
            ev2, vals2 = win2.Read()
            if ev2 == sg.WIN_CLOSED or ev2 == 'Cancel':
                win2.Close()
                win2_active = False
                win1.UnHide()
            if ev2 == 'Submit':
                win2.Close()
                win2_active = False
                win1.UnHide()
