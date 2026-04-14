from agents.swarm import Context, Swarm
from core.world_model import World

swarm = Swarm()
world = World()


def run(e):
    world.update(e)
    ctx = Context(state=e, memory=world.memory)
    return swarm.step(ctx)
