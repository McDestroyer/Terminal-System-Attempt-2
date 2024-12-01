from system.objects.helper_objects import pixel_grid
from system.objects.system_objects import display


class DisplayManager:
    def __init__(self, display_grid: pixel_grid.PixelGrid) -> None:
        self.display = display.Display(display_grid)

    def update(self):
        self.display.anti_flash_refresh_display()
