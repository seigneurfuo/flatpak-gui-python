import subprocess
import shlex
from distutils import spawn

class Flatpyk:
    def __init__(self):
            self.flatpak_executable_found = spawn.find_executable("flatpak") is not None

    def _execute_cli(self, cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return_code = process.returncode
        return stdout.decode("utf-8"), stderr, return_code

    def _parse_output(self, text):
        return [row.split("\t") for row in text.split("\n") if row]

    def list_installed(self, filters=[]):
        cmd = "flatpak list"

        if filters:
            if "apps" in filters:
                cmd += " --app --columns=name,application,version,branch,size,installation,runtime,origin"

            elif "runtimes" in filters:
                cmd += " --runtime --columns=name,application,version,branch,size,installation"

        stdout, stderr, return_code = self._execute_cli(cmd)
        return self._parse_output(stdout)

    def list_availables(self, filters=[]):
        cmd = "flatpak remote-ls"

        if filters:
            if "apps" in filters:
                cmd += " --app --columns=name,application,version,branch,installed-size,runtime,origin"

            elif "runtimes" in filters:
                cmd += " --runtime --columns=name,application,version,branch,installed-size"

        stdout, stderr, return_code = self._execute_cli(cmd)
        return self._parse_output(stdout)

    def list_remotes(self):
        cmd = "flatpak remote --columns=name,title,url,homepage"
        stdout, stderr, return_code = self._execute_cli(cmd)
        return self._parse_output(stdout)

    def run(self, flatpak_id) -> None:
        cmd = ["flatpak", "run", flatpak_id]
        subprocess.Popen(cmd)

        # TODO: Erreurs et +

    def gui_terminal(self, cmd, sleep=2) -> None:
        cmd = ["xterm", "-e", cmd]
        subprocess.call(cmd)

    def install(self, packages: list) -> None:
        cmd = "flatpak install {}; sleep {}".format("".join(packages))
        print(cmd)
        self.gui_terminal(cmd, sleep=2)

if __name__ == "__main__":
    flatpyk = Flatpyk()
    t = flatpyk.list_installed()
    print(t)