import time

from system.inputs.mouse_handler import MouseHandler

mouse = MouseHandler()

while True:
    # print(mouse.is_focused())
    mouse.update_inputs()

    print(mouse._is_clicked)


    time.sleep(0.1)
