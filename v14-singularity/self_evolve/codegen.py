class CodeGen:
    def generate(self, prompt: str) -> str:
        return f"# generated\nprint('task:{prompt}')\n"
