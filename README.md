# LiveScan: Self-Evolving Graph Intelligence System

LiveScan is a production-oriented AI system combining temporal graph modeling, graph transformers, decision transformers, Bayesian uncertainty, and adaptive routing for online/offline learning.

## Features
- Temporal graph builder (stream to dynamic graph tensors)
- Multi-model fusion: GNN + Graph Transformer + Decision Transformer + DeepSets encoder
- Bayesian uncertainty with MC dropout and predictive variance
- Online learning loop and offline trainer
- FastAPI inference API with Prometheus metrics
- Kafka ingestion + Flink SQL job definitions
- Feast feature store integration
- Docker, Kubernetes manifests, Helm chart, and CI pipeline

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn livescan.api.main:app --host 0.0.0.0 --port 8000
```

## Final release installer setup + configuration
```bash
cp scripts/release_installer.env.example scripts/release_installer.env
# optional: edit scripts/release_installer.env
bash scripts/release_installer.sh
```

To run a wheel-based release install, set `INSTALL_MODE=release` in
`scripts/release_installer.env`. To auto-start the API after install,
set `START_API=true`.

## Offline train
```bash
python scripts/train_offline.py
```

## Tests
```bash
pytest -q
```

## Reference architecture blueprints
- `v11-agi/`: merged AGI-style sovereign platform blueprint.
- `v12-civilization-ai/`: civilization-scale autonomous AI blueprint.
