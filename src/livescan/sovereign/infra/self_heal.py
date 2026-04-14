import subprocess


class SelfHealer:
    """Checks cluster health and restarts a deployment on crash loops."""

    def __init__(self, deployment: str = "deployment/inference") -> None:
        self.deployment = deployment

    def check(self) -> bool:
        try:
            result = subprocess.run(["kubectl", "get", "pods"], capture_output=True, text=True, check=False)
        except FileNotFoundError:
            return False
        if "CrashLoopBackOff" in result.stdout:
            self.recover()
            return True
        return False

    def recover(self) -> None:
        subprocess.run(["kubectl", "rollout", "restart", self.deployment], check=False)
