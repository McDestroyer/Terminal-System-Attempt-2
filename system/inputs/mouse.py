from pynput import mouse

ms = mouse.Controller()

# Get the mouse position
print('The current pointer position is {0}'.format(ms.position))

mouse.Events.get()