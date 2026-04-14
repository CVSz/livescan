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
        return {"plan": "optimize_policy"}


class Executor(Agent):
    def act(self, ctx):
        return {"action": "execute"}


class Critic(Agent):
    def act(self, ctx):
        return {"reward": ctx.state.get("reward", 0)}


class Auditor(Agent):
    def act(self, ctx):
        u = float(ctx.state.get("uncertainty", 0.0))
        return {"risk_score": u}


class Swarm:
    def __init__(self):
        self.agents = [Planner(), Executor(), Critic(), Auditor()]

    def step(self, ctx: Context):
        out = {}
        for a in self.agents:
            out.update(a.act(ctx))
        return out
