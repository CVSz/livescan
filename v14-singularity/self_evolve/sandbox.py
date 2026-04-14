import os
import subprocess
import tempfile


class Sandbox:
    """Execute generated code in a temp directory."""

    def run(self, code: str):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "run.py")
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
            return subprocess.run(["python", path], capture_output=True, text=True, timeout=3)
