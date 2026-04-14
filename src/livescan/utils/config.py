from pydantic import BaseModel


class RuntimeConfig(BaseModel):
    model_dim: int = 64
    num_heads: int = 4
    num_layers: int = 3
    max_nodes: int = 128
    action_dim: int = 8
    learning_rate: float = 3e-4
    online_batch_size: int = 32
    mc_samples: int = 8
    feature_repo_path: str = "./feature_repo"


CONFIG = RuntimeConfig()
