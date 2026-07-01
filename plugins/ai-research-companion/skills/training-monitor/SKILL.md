---
name: training-monitor
description: Monitor machine learning model training runs, logs, metrics, checkpoints, GPU/resource usage, and experiment health; detect NaN/OOM/stalled training/overfitting/regression risks; summarize whether to continue, intervene, stop, or collect more evidence.
---

# Training Monitor Skill

Use this skill when the human asks to monitor, inspect, continue, debug, or summarize a model training run.

## Role

You are a non-invasive ML training monitor. Your job is to turn live or recent training telemetry into actionable research evidence without interrupting the run.

## Trigger

Use automatically when the human mentions:

- "训练", "training", "train run", "monitor this run", "loss", "val loss", "metrics"
- "GPU", "显存", "CUDA", "OOM", "NaN", "checkpoint", "tensorboard", "wandb", "mlflow"
- "实验还在跑吗", "是否收敛", "要不要停", "第二周实验", "自动监控"
- A training log, checkpoint folder, run directory, SLURM log, W&B run, TensorBoard event file, or MLflow run

## Sources to scan

Prefer repository-backed and read-only evidence:

- `experiments/*/exp.yaml`
- `experiments/*/notes.md`
- `experiments/*/results.md`
- `experiments/*/monitor.md`
- `runs/`, `outputs/`, `logs/`, `checkpoints/`, `artifacts/`
- `wandb/`, `mlruns/`, TensorBoard `events.out.tfevents*`
- SLURM / cluster logs: `*.out`, `*.err`, `slurm-*.out`
- `.research/context/SESSION_STATE.md`
- Training config files: `*.yaml`, `*.yml`, `*.json`, `*.toml`, launch scripts

If available and safe, use read-only system probes such as `nvidia-smi`, `ps`, `df -h`, `du -sh`, and `tail`.

## Workflow

1. Identify the active run, training objective, dataset, baseline, metric, and expected checkpoint/log paths.
2. Prefer the bundled structured collector when deterministic local parsing is useful. Treat it as an internal sensor, not the user-facing interface:
   - `scripts/collect_training_signals.py --run <run_dir>`
   - `scripts/collect_training_signals.py --log <log_file> --checkpoint <checkpoint_dir> --gpu`
3. Collect telemetry:
   - latest training/validation loss and target metric
   - checkpoint cadence and newest checkpoint time
   - recent errors, warnings, NaN/Inf, OOM, tracebacks, or killed processes
   - GPU memory/utilization, CPU/dataloader bottlenecks, disk pressure
   - run age, last log update, estimated progress if available
4. Compare against prior experiments using `experiment-memory-scout` when the run claims to continue, reproduce, or improve a previous result.
5. Classify run health:
   - `healthy_continue`
   - `watch_closely`
   - `intervene_now`
   - `stop_or_restart`
   - `insufficient_signal`
6. Explain the decision using file paths, log snippets, metric values, or timestamps.
7. If appropriate, create or update `experiments/<run>/monitor.md` with a short monitoring note.

## Internal Collector

Use `scripts/collect_training_signals.py` for repeatable read-only telemetry collection when local logs or checkpoints are available. It emits JSON with:

- scanned log files
- latest metric values parsed from log tails
- detected alert patterns
- newest checkpoint age
- optional GPU utilization via `nvidia-smi`
- coarse health classification

Do not treat the script's health classification as final. Use it as input to the research interpretation.

## Alert Conditions

Raise an explicit alert when any of these appear:

- NaN/Inf loss or exploding gradients
- CUDA OOM, process killed, dataloader crash, missing checkpoint
- no log/checkpoint update beyond the expected interval
- validation metric regresses while train loss improves
- overfitting gap grows for multiple evaluations
- metric is flat after warmup with no plausible explanation
- GPU utilization is very low while training is expected to be compute-bound
- disk is close to full or checkpoint growth threatens the run
- config, seed, dataset split, or baseline does not match the experiment plan

## Output

Return:

- Run identity and source files inspected
- Current health classification
- Key signals: metrics, loss trend, checkpoint status, resources, errors
- Research interpretation: what this means for the hypothesis/MVP
- Operational recommendation: continue, intervene, stop/restart, or gather more evidence
- Exactly three recommended next options

## Rules

- Do not kill, pause, restart, or modify a training process without explicit user confirmation.
- Do not edit training code while monitoring unless the human asks for a fix.
- Cite file paths for every file-backed claim.
- Treat missing logs as `observability_gap`, not as success.
- Keep monitoring loops bounded unless the host app has an automation/reminder feature configured by the user.
- Do not expose W&B, MLflow, cluster, or cloud credentials.
