# LabBench FigQA Solver

Improve a scientific figure QA solver to maximize accuracy on LabBench FigQA.

## Setup

1. **Read the in-scope files**: The repo is small. Read these files for full context:
   - `agent.py` — the file you modify. The figure QA solver.
   - `eval/eval.sh` — runs evaluation. Do not modify.
   - `prepare.sh` — downloads LabBench FigQA dataset + images. Do not modify.
2. **Run prepare**: `bash prepare.sh` to download the dataset. This saves images to `data/images/`.
3. **Verify data exists**: Check that `data/` contains `test.jsonl` and `data/images/` has .jpg files.
4. **Initialize results.tsv**: Create `results.tsv` with just the header row.
5. **Run baseline**: `bash eval/eval.sh` to establish the starting accuracy.

## The benchmark

LabBench FigQA tests understanding of scientific figures from research papers. Each question presents:
- A scientific figure (chart, graph, microscopy image, etc.)
- A multiple choice question about the figure (A/B/C/D/E)

Total: **181 test problems**. The agent receives the image as base64 via the OpenAI vision API and must output the correct letter.

**Note**: This task requires a **vision model** (e.g., gpt-4o, gpt-4.1-mini). Set `SOLVER_MODEL` to a model that supports image input.

## Experimentation

**What you CAN do:**
- Modify `agent.py` — this is the only file you edit. Everything is fair game: prompting strategy, image analysis approach, chain-of-thought before answering, asking the model to describe the figure first.

**What you CANNOT do:**
- Modify `eval/`, `prepare.sh`, or test data.
- Change the model. The model is fixed (set via `SOLVER_MODEL` env var).
- Install new packages beyond what's in `requirements.txt`.

**The goal: maximize accuracy.** Each answer is a single letter. Exact letter match. Accuracy = fraction correct.

**Cost** is a soft constraint. Some increase in API calls is acceptable for meaningful gains.

**Simplicity criterion**: All else being equal, simpler is better.

## Output format

The eval prints a summary:

```
---
accuracy:         0.4200
correct:          76
total:            181
```

## Logging results

Log each experiment to `results.tsv` (tab-separated):

```
commit	accuracy	cost_usd	status	description
a1b2c3d	0.420000	2.10	keep	baseline
b2c3d4e	0.510000	3.40	keep	describe figure first, then answer
```

## The experiment loop

LOOP FOREVER:

1. **THINK** — decide what to try next. Review your results.tsv. Scientific figures require careful reading — consider having the model describe what it sees before answering.
2. Modify `agent.py` with your experimental idea.
3. git commit
4. Run the experiment: `bash eval/eval.sh > run.log 2>&1`
5. Read out the results: `grep "^accuracy:" run.log`
6. If the grep output is empty, the run crashed. Run `tail -n 50 run.log` for the stack trace and attempt a fix.
7. Record the results in results.tsv (do not commit results.tsv).
8. If accuracy improved (higher), keep the git commit. If equal or worse, `git reset --hard HEAD~1`.

**Timeout**: If a run exceeds 60 minutes, kill it and treat it as a failure.

**NEVER STOP**: Once the loop begins, do NOT pause to ask the human. You are autonomous. The loop runs until interrupted.
