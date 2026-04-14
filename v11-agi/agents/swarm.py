from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Context:
    state: Dict[str, Any]
    history: list


class Agent:
    def act(self, ctx: Context):
        raise NotImplementedError


class Planner(Agent):
    def act(self, ctx: Context):
        return {"plan": "optimize_policy"}


class Executor(Agent):
    def act(self, ctx: Context):
        return {"action": "execute_policy"}


class Critic(Agent):
    def act(self, ctx: Context):
        return {"reward": ctx.state.get("reward", 0)}


class Auditor(Agent):
    def act(self, ctx: Context):
        uncertainty = ctx.state.get("uncertainty", 0)
        return {"risk": "HIGH" if uncertainty > 0.7 else "LOW"}


class Swarm:
    def __init__(self):
        self.agents = [Planner(), Executor(), Critic(), Auditor()]

    def step(self, ctx: Context):
        return {agent.__class__.__name__: agent.act(ctx) for agent in self.agents}
