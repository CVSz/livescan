from agents.swarm import Context, Swarm
from core.policy_engine import PolicyEngine
from core.world_model import World

swarm = Swarm()
world = World()
policy = PolicyEngine()


def run(e: dict):
    world.update(e)
    ctx = Context(state=e, memory=world.memory)

    decision = swarm.step(ctx)
    decision["estimated_cost"] = float(e.get("cost", 0.0))

    verdict = policy.validate(decision)
    decision["allowed"] = verdict["allowed"]
    if not verdict["allowed"]:
        decision["reason"] = verdict["reason"]

    return decision
