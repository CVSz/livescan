from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Context:
    state: dict[str, Any]
    history: list[dict[str, Any]]


class Agent:
    def act(self, ctx: Context) -> dict[str, Any]:
        raise NotImplementedError


class Planner(Agent):
    def act(self, ctx: Context) -> dict[str, Any]:
        uncertainty = float(ctx.state.get("uncertainty", 0.0))
        plan = "exploit_policy" if uncertainty < 0.3 else "analyze_pattern_and_adjust_policy"
        return {"plan": plan}


class Executor(Agent):
    def act(self, ctx: Context) -> dict[str, Any]:
        plan = ctx.state.get("plan", "apply_policy")
        return {"action": plan if isinstance(plan, str) else "apply_policy"}


class Critic(Agent):
    def act(self, ctx: Context) -> dict[str, Any]:
        return {"score": float(ctx.state.get("reward", 0.0))}


class Auditor(Agent):
    def act(self, ctx: Context) -> dict[str, Any]:
        risk = "LOW" if float(ctx.state.get("uncertainty", 0.0)) < 0.5 else "HIGH"
        return {"risk": risk}


class Swarm:
    def __init__(self) -> None:
        self.agents: list[Agent] = [Planner(), Executor(), Critic(), Auditor()]

    def step(self, ctx: Context) -> dict[str, dict[str, Any]]:
        return {agent.__class__.__name__: agent.act(ctx) for agent in self.agents}
