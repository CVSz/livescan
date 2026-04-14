from typing import Any, Dict


class PolicyEngine:
    """Enforce hard constraints and provide verifiable decisions."""

    MAX_RISK = 0.7
    MAX_COST = 1000.0

    def validate(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        risk = float(decision.get("risk_score", 0.0))
        cost = float(decision.get("estimated_cost", 0.0))

        if risk > self.MAX_RISK:
            return {"allowed": False, "reason": "RISK_LIMIT"}

        if cost > self.MAX_COST:
            return {"allowed": False, "reason": "COST_LIMIT"}

        return {"allowed": True}
