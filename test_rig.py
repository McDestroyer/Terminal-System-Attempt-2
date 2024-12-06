import time

import system.objects.helper_objects.ascii_image as image
import system.objects.helper_objects.coordinate_objects.coordinate as coord
from system.utilities import cursor


def test_ascii_image():

    start_time = time.time()
    # Create an image object.
    img = image.Image(coord.Coordinate(), "C:\\Users\\dafan\\OneDrive\\Desktop\\CS\\Side Project Games and Apps\\Terminal System Attempt 2\\system\\assets\\images\\flashing_logo.AAI")

    print(f"Time to create image: {time.time() - start_time}")
    # Update the image.
    img.update_animation()

    # Print the image to the terminal.
    print(img.grid)

    time.sleep(1)

    # Update the image.
    img.update_animation()

    # Print the image to the terminal.
    print(img.grid)
    cursor.clear_screen()
    cursor.hide()
    cursor.set_pos()

    while True:
        img.update_animation()
        print(img.to_string())
        cursor.set_pos()
        # print("\n----------\n")
        time.sleep(.5)


if __name__ == '__main__':
    test_ascii_image()
