import subprocess
import uuid


class CodeGen:
    """
    Generates and executes simple modules for self-evolution experiments.
    """

    def generate(self, prompt: str):
        filename = f"gen_{uuid.uuid4().hex}.py"
        code = f"# auto-generated\\nprint('{prompt}')"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(code)

        return filename

    def deploy(self, file):
        subprocess.run(["python", file], check=False)
