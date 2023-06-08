import subprocess
import shlex
from distutils import spawn

from terminal import Terminal

class Flatpyk:
    def __init__(self):
        self.flatpak_executable_path = spawn.find_executable("flatpak")
        self.flatpak_executable_found = self.flatpak_executable_path is not None
        self.terminal = Terminal()
        #self.terminal.get_default_terminal()

        self.availables_packages_cache = []
        self.availables_runtimes_cache = []

    def _execute_cli(self, cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return_code = process.returncode
        return stdout.decode("utf-8"), stderr, return_code

    def _parse_output(self, text):
        return [row.split("\t") for row in text.split("\n") if row]

    def _search_filter_package_name(self, results, search):
        filtered_results = []
        for item_index, item in enumerate(results):
            if item[0].lower().startswith(search.lower()) or item[1].lower().startswith(search.lower()):
                filtered_results.append(item)

        return filtered_results

    def list_installed(self, filters=[], search=None):
        cmd = f"{self.flatpak_executable_path} list"

        if filters:
            if "apps" in filters:
                cmd += " --app --columns=name,application,version,branch,size,installation,runtime,origin"

            elif "runtimes" in filters:
                cmd += " --runtime --columns=name,application,version,branch,size,installation"

        stdout, stderr, return_code = self._execute_cli(cmd)
        results = self._parse_output(stdout)

        if search:
            results = self._search_filter_package_name(results, search)
        
        return results

    def list_availables(self, filters=[], search=None, use_cached=False):
        cmd = f"{self.flatpak_executable_path} remote-ls"

        # FIltre obligatoires: TODO: All
        if not filters:
            return []

        if "apps" in filters:
            if not (self.availables_packages_cache and use_cached):
                print("Generating cache for available apps")

                cmd += " --app --columns=name,application,version,branch,installed-size,runtime,origin"
                stdout, stderr, return_code = self._execute_cli(cmd)
                self.availables_packages_cache = self._parse_output(stdout)
                
            results = self.availables_packages_cache

        elif "runtimes" in filters:
            if not (self.availables_runtimes_cache or use_cached):
                print("Generating cache for available runtimes")

                cmd += " --runtime --columns=name,application,version,branch,installed-size"
                stdout, stderr, return_code = self._execute_cli(cmd)
                self.availables_runtimes_cache = self._parse_output(stdout)
                
            results = self.availables_runtimes_cache

        if search:
            results = self._search_filter_package_name(results, search)

        return results

    def list_remotes(self):
        cmd = f"{self.flatpak_executable_path} remote --columns=name,title,url,homepage"
        stdout, stderr, return_code = self._execute_cli(cmd)
        return self._parse_output(stdout)

    def run(self, flatpak_id: str) -> None:
        cmd = [self.flatpak_executable_path, "run", flatpak_id]
        subprocess.Popen(cmd)

        # TODO: Erreurs et +

    def gui_terminal(self, cmd: str, sleep=2) -> None:
        # TODO: Sleep
        cmd = self.terminal.default_terminal.split(" ") + [cmd]
        subprocess.call(cmd)

    def install(self, packages: list) -> None:
        cmd = "{} install {} && sleep 2".format(self.flatpak_executable_path, "".join(packages))
        print(cmd)
        self.gui_terminal(cmd, sleep=2)