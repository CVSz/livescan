from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Context:
    state: Dict[str, Any]
    world: Dict[str, Any]


class Agent:
    def act(self, ctx: Context):
        raise NotImplementedError


class Economist(Agent):
    def act(self, ctx: Context):
        return {"market_adjustment": ctx.world.get("capital", 0) * 0.01}


class Governor(Agent):
    def act(self, ctx: Context):
        risk = ctx.world.get("risk", 0)
        return {"policy": "stabilize" if risk < 0.5 else "restrict"}


class Civilization:
    def __init__(self):
        self.agents = [Economist(), Governor()]

    def step(self, ctx: Context):
        return {agent.__class__.__name__: agent.act(ctx) for agent in self.agents}
