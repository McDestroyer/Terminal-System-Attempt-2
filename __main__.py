from example_program.main import Main
from system.utilities.personal_functions import error


if __name__ == '__main__':
    main = None
    try:
        main = Main()
        main.loop()
        main.shutdown()
    except KeyboardInterrupt as e:
        error(f"You're killing me!")
        main.shutdown()
