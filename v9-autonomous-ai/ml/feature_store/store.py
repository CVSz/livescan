from __future__ import annotations

from feast import FeatureStore

store = FeatureStore(repo_path=".")


def get_features(entity_rows: list[dict]) -> dict:
    return store.get_online_features(
        features=["spin_features:cascade", "spin_features:multiplier"],
        entity_rows=entity_rows,
    ).to_dict()
