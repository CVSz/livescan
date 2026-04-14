from typing import Any

from feast import FeatureStore

from livescan.utils.config import CONFIG
from livescan.utils.logging import build_logger

logger = build_logger("feature-store")


class FeastFeatureClient:
    def __init__(self, repo_path: str | None = None):
        self.repo_path = repo_path or CONFIG.feature_repo_path
        self.store = FeatureStore(repo_path=self.repo_path)

    def get_online_features(self, entity_rows: list[dict[str, Any]], features: list[str]) -> dict[str, Any]:
        result = self.store.get_online_features(features=features, entity_rows=entity_rows).to_dict()
        logger.info("feature_fetch", extra={"entities": len(entity_rows), "features": features})
        return result
