from agents.swarm import Context, Swarm
from core.world import World

swarm = Swarm()
world = World()


def run(event):
    world.update(event)
    ctx = Context(state=event, history=world.memory)
    return swarm.step(ctx)
