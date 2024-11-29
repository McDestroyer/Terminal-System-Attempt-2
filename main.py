import system.terminal_system as terminal_system

if __name__ == '__main__':
    terminal_system = terminal_system.TerminalSystem()

    while terminal_system.run:
        try:
            terminal_system.update()

            terminal_system.output()

        except KeyboardInterrupt as e:
            print(f'Exception in terminal_system.main_loop():\n{e}')
            terminal_system.shutdown()
