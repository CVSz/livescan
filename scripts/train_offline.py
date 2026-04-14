import torch

from livescan.models.fusion import AdaptiveFusionModel
from livescan.training.engine import OfflineTrainer


def synthetic_dataset(num_batches: int = 8, max_nodes: int = 128, feature_dim: int = 16, action_dim: int = 8):
    dataset = []
    for _ in range(num_batches):
        node_features = torch.randn(max_nodes, feature_dim)
        adjacency = torch.randint(0, 2, (max_nodes, max_nodes)).float()
        returns = torch.randn(1).abs()
        labels = torch.randint(0, action_dim, (1,))
        dataset.append(
            {
                "node_features": node_features,
                "adjacency": adjacency,
                "returns_to_go": returns,
                "labels": labels,
            }
        )
    return dataset


if __name__ == "__main__":
    model = AdaptiveFusionModel(in_dim=16, action_dim=8, model_dim=64, heads=4, layers=2)
    trainer = OfflineTrainer(model)
    losses = trainer.run_epochs(synthetic_dataset(), epochs=2)
    print({"batches": len(losses), "last_loss": losses[-1]})
