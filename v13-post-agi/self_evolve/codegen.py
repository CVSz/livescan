import subprocess
import uuid


class CodeGen:
    def generate(self, prompt):
        f = f"gen_{uuid.uuid4().hex}.py"
        with open(f, "w", encoding="utf-8") as fp:
            fp.write(f"print('{prompt}')")
        return f

    def run(self, f):
        subprocess.run(["python", f], check=False)
