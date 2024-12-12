import socket
import threading

from pynput import mouse


class MouseBlocker:

    def __init__(self, window_rect: dict[str, int]) -> None:
        """Initialize the mouse blocker.

        Args:
            window_rect (dict[str, int]):
                The window rectangle.
        """
        self.window_rect = window_rect

        self.mouse_position = (0, 0)
        self.is_clicked = False
        self.block_mouse = False

        self.mouse_listener = mouse.Listener(win32_event_filter=self._win32_event_filter)
        self.mouse_listener.start()

        self.socket_listener = threading.Thread(target=self.socket_listener, daemon=True)
        self.socket_listener.start()

    def socket_listener(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 65432))
        server_socket.listen()

        print("Socket server is listening...")
        conn, addr = server_socket.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode()
                if command == 'unblock':
                    self.block_mouse = False
                    # print("Mouse inputs are now unblocked.")
                elif command == 'block':
                    self.block_mouse = True
                    # print("Mouse inputs are now blocked.")
                elif command == 'exit':
                    break
                elif command.startswith('update_window_rect'):
                    window_rect = command.split(' ')[1:]
                    self.window_rect = {
                        "left": int(window_rect[0]),
                        "top": int(window_rect[1]),
                        "right": int(window_rect[2]),
                        "bottom": int(window_rect[3])
                    }
                elif command == 'update_mouse_position':
                    mouse_position = command.split(' ')[1:]
                    self.mouse_position = (int(mouse_position[0]), int(mouse_position[1]))
                else:
                    pass
                if self.is_clicked:
                    print("Mouse is clicked.")
                else:
                    print("Mouse is not clicked.")
                conn.sendall(("mouse_clicked: " + str(self.is_clicked)).encode())

    def _win32_event_filter(self, msg, _) -> bool:
        """Filter the win32 events.

        Args:
            msg (int):
                The message of the event.
            _ (int):
                The data of the event.

        Returns:
            bool: Whether the event was filtered or not.
        """
        # Suppress Left click
        if self.block_mouse and (msg == 513 or msg == 514) and self.window_rect and (
                self.window_rect["left"] < self.mouse_position[0] < self.window_rect["right"] and
                self.window_rect["top"] < self.mouse_position[1] < self.window_rect["bottom"]
        ):
            self.is_clicked = True if msg == 513 else False if msg == 514 else self.is_clicked
            self.mouse_listener.suppress_event()
        return True


if __name__ == "__main__":
    mouse_blocker = MouseBlocker({"left": 0, "top": 0, "right": 100, "bottom": 100})

    while True:
        pass
