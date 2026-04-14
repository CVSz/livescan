from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Context:
    state: Dict[str, Any]
    memory: list


class Agent:
    def act(self, ctx: Context):
        raise NotImplementedError


class Planner(Agent):
    def act(self, ctx):
        return {"plan": "optimize"}


class Executor(Agent):
    def act(self, ctx):
        return {"execute": True}


class Critic(Agent):
    def act(self, ctx):
        return {"reward": ctx.state.get("reward", 0)}


class Auditor(Agent):
    def act(self, ctx):
        risk = ctx.state.get("uncertainty", 0)
        return {"risk": "HIGH" if risk > 0.7 else "LOW"}


class Swarm:
    def __init__(self):
        self.agents = [Planner(), Executor(), Critic(), Auditor()]

    def step(self, ctx):
        return {a.__class__.__name__: a.act(ctx) for a in self.agents}
