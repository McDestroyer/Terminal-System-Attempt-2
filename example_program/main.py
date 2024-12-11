import copy
import time

from system.terminal_system import TerminalSystem

from system.objects.system_objects.screen_object import Screen

from system.objects.helper_objects.ascii_image import Image
from system.objects.helper_objects.ascii_text import Text
from system.objects.helper_objects.coordinate_objects.axis import Axis
from system.objects.helper_objects.coordinate_objects.coordinate import Coordinate
from system.objects.helper_objects.coordinate_objects.point import Point
from system.objects.helper_objects.formatted_text import FormattedText
from system.objects.helper_objects.pixel_objects.pixel import Pixel
from system.objects.helper_objects.pixel_objects.pixel_theme import ThemeDict, ThemeTypes, PixelTheme

from system.objects.terminal_objects.image_object import ImageObject
from system.objects.terminal_objects.text_object import TextObject

from system.utilities.color import Colors


class Main:
    """Main class for the example program."""

    def __init__(self) -> None:
        """Initialize an instance of the class."""
        self.run = True

        self._terminal = TerminalSystem(
            name="Example Program",
            minimum_screen_size=Point(50, 20),
            desired_fps=30,
            mouse_enabled=True,
            in_editor=True,
        )

        home_screen = Screen("home", self._terminal.initial_pixel_grid)

        self._terminal.display_manager.add_screen(home_screen)
        self._terminal.display_manager.set_current_screen("home")

        # Construct the test image object.
        test_image_object_image = Image(
            coordinates=Coordinate(),
            image_frames="C:\\Users\\dafan\\OneDrive\\Desktop\\CS\\Side Project Games and Apps" +
                         "\\Terminal System Attempt 2\\system\\assets\\images\\flashing_logo.AAI",
        )

        test_image_object = ImageObject(
            name="Test Image",
            description="Test Image",
            image=test_image_object_image,
            initial_grid=copy.deepcopy(self._terminal.initial_pixel_grid),
        )

        test_image_object.grid.coordinates.x_char = 10
        test_image_object.grid.coordinates.y_char = 15

        self._terminal.display_manager.get_current_screen().add_object(test_image_object)

        # Construct the test text object.

        test_text_object_text = Text(
            coordinates=Coordinate(),
            size=Coordinate(),
            text=FormattedText(
                text_list=[("This is a test text object.", ThemeDict(
                    {ThemeTypes.DEFAULT: PixelTheme(
                        [Colors.GREEN, Colors.BACKGROUND_BLACK]
                    )}))],
                wrap_words=False,
            ),
        )

        text_grid = copy.deepcopy(self._terminal.initial_pixel_grid)
        text_grid.default_pixel = Pixel(
            char="#",
            themes=ThemeDict(
                {ThemeTypes.DEFAULT: PixelTheme(
                    [Colors.BRIGHT_GREEN, Colors.BACKGROUND_BLACK]
                )}
            ),
        )

        test_text_object = TextObject(
            name="Test Text",
            description="Test Text",
            text=test_text_object_text,
            initial_grid=self._terminal.initial_pixel_grid,
            z_index=1,
        )

        test_text_object.move(Coordinate(Axis(20), Axis(25)))
        test_text_object.resize(Coordinate(Axis(25), Axis(4)))

        self._terminal.display_manager.get_current_screen().add_object(test_text_object)

        # Add any other code to initialize here.
        self.last_time = time.time()
        self.previous_times = []

    def loop(self) -> None:
        """Run the program."""
        while self.run:
            update_start_time = time.time()
            self._terminal.update()
            print(f"Update Time: {(time.time() - update_start_time) * 1000}ms")

            # Add the code to run here.
            refresh_start_time = time.time()
            self._terminal.refresh_screen()
            print(f"Refresh Time: {(time.time() - refresh_start_time) * 1000}ms")

            loop_time = 1 / (time.time() - update_start_time)
            self.previous_times.append(loop_time)
            if len(self.previous_times) > 100:
                self.previous_times.pop(0)
            print(f"Average FPS: {sum(self.previous_times) / len(self.previous_times)}")
            print(f"FPS: {1 / (time.time() - self.last_time)}")
            self.last_time = time.time()

            # print(self._terminal.display_manager.get_current_screen().terminal_objects[0].grid.grid)
            # print(self._terminal.display_manager.get_current_screen().terminal_objects[0].visible)

    def shutdown(self) -> None:
        """Stop the program."""
        self._terminal.shutdown()
