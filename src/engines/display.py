import curses


class Display:
    def __init__(self, app):
        self.app = app
        self.console = curses.initscr()
        curses.noecho()
        self.line_length = 120

    def update(self, state: dict):
        try:
            self.console.clear()
            self.console.addstr("┌" + ("─"*(self.line_length - 2)) + "┐" + "\n")
            for key, value in state.items():
                if key[:5] == "empty":
                    line_str = ""
                else:
                    line_str = f"{key} : {value}"
                if key[0] == "l":
                    # Align left
                    self.console.addstr("│ " + line_str[1:] + " "*(self.line_length//2 - 2 - len(line_str[1:])))
                else:
                    # Align right
                    self.console.addstr(" "*(self.line_length//2 - 2 - len(line_str)) + line_str + " │\n")
                
            self.console.addstr("└" + ("─"*(self.line_length - 2)) + "┘")
            self.console.refresh()
        except:
            # Terminal window is not big enough to display
            pass

    def destroy(self):
        curses.nocbreak()
        self.console.keypad(0)
        curses.echo()
        curses.endwin()
