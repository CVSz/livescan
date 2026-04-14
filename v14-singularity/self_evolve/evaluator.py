class Evaluator:
    def score(self, stdout: str, stderr: str) -> float:
        return float(len(stdout)) - float(len(stderr))
