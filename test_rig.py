import time

from system.inputs.mouse_handler import MouseHandler

mouse = MouseHandler()

while True:
    # print(mouse.is_focused())
    mouse.update_inputs()
    print(mouse.get_inputs())
    print(mouse.listener.is_alive())
    time.sleep(0.1)
