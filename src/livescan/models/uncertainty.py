import torch


def mc_dropout_predict(model, inputs: dict, samples: int = 8):
    model.train()
    preds = []
    with torch.no_grad():
        for _ in range(samples):
            logits, route = model(**inputs)
            preds.append(logits)
    stack = torch.stack(preds, dim=0)
    mean = stack.mean(dim=0)
    variance = stack.var(dim=0).mean().item()
    model.eval()
    return mean, variance, route
