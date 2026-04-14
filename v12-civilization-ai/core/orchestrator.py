from agents.civilization import Civilization, Context
from core.world_model import WorldModel
from economy.market import Market

world = WorldModel()
civ = Civilization()
market = Market()


def run(event):
    world.update(event)

    ctx = Context(state=event, world={"capital": world.resources["capital"]})
    agent_out = civ.step(ctx)

    price = market.update(demand=event.get("demand", 1), supply=event.get("supply", 1))

    return {
        "agents": agent_out,
        "market_price": price,
        "resources": world.resources,
    }
