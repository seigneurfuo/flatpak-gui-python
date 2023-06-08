import os
from distutils import spawn

class Terminal:
    def __init__(self):
        self.ignored_executables = []
        xterm_executable = spawn.find_executable("xterm")
        if not xterm_executable:
            exit(1)

        self.fallback_terminal = f"{xterm_executable} -e"
        self.default_terminal = self.fallback_terminal

    def get_default_terminal(self, ignore=[]):
        if not ignore:
            ignore = self.ignored_executables

        terminal_executables = [
            {"name": "gnome-terminal", "args": ""},
            {"name": "konsole", "args": ""},
            {"name": "mate-terminal", "args": "--execute"},
            {"name": "xfce4-terminal", "args": "--execute"}
        ]

        for executable in terminal_executables:
            if executable["name"] in ignore:
                continue

            executable_path = spawn.find_executable(executable["name"])
            if executable_path:
                print("Trouvé", executable)
                self.default_terminal = f"{executable_path} {executable['args']}"
                break

            else:
                print("Pas trouvé", executable)

        return self.default_terminal


if __name__ == "__main__":
    terminal = Terminal()
    terminal.get_default_terminal(ignore=["mate-terminal"])

    print(terminal.default_terminal)
