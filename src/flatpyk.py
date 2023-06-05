import subprocess

class Flatpyk:
    def __init__(self):
        pass

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

if __name__ == "__main__":
    flatpyk = Flatpyk()
    t = flatpyk.list_installed()
    print(t)