from __future__ import annotations

from livescan.sovereign.agents.swarm import Context, Swarm
from livescan.sovereign.ml.world_model import WorldModel

swarm = Swarm()
world = WorldModel()


def loop(event: dict[str, float]) -> dict[str, dict[str, float | str]]:
    world.update(event)
    ctx = Context(state=event, history=world.memory)
    return swarm.step(ctx)
