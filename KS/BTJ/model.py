from typing import Tuple
from operator import itemgetter
from math import log, exp
import json

# APR
# base_constants: [1.75, 1.95, 1]
# (101): 0.25(A) + 0.15(A) + 0.15(R) + 0.5 * 0.4(R) = 1.75
# (102): 0.25(A) + 0.3(R) + 0.15(P) + 0.5 * 0.5 = 1.95
# (211): 1

# Conditionals
# (102): 0.5 * 0.4 * (1 - 0.875)(A)
# (211): 0.5 * 0.875 * (1 - 0.4)(P)

A = 0.4 * (1 - 0.875)
B = 0.875 * (1 - 0.4)

MAX_COUNT = 4
LABELS = ("C", "A", "V")

def load_run(path):
    with open(path) as f:
        data = json.load(f)
    data["data"] = {
        tuple(sorted(key.split(), key=lambda t: LABELS.index(t[-1]))): value
        for key, value in data["data"].items()
    }
    return data

def convert_combo(combo: Tuple[int, int, int]) -> Tuple[str, ...]:
    return tuple(f"{c}{label}" for c, label in zip(combo, LABELS) if c != 0)

def compute_multiplier(constants, steps, counts):
    assert len(constants) == len(steps) == len(counts) == 3
    return ((constants[0] + steps[0] * counts[0]) *
            ((constants[1] + 0.5 * A) + steps[1] * counts[1]) *
            ((constants[2] + 0.5 * B) + (1 - B) * steps[2] * min(counts[2], 1)))

def iterate_combinations():
    return [(i, j, MAX_COUNT - i - j)
            for i in range(MAX_COUNT + 1)
            for j in range(MAX_COUNT - i + 1)]

def find_max(constants, steps):
    scored = (
        (convert_combo(combo), compute_multiplier(constants, steps, combo))
        for combo in iterate_combinations()
    )
    return dict(sorted(scored, key=itemgetter(1), reverse=True))

def relative_errors(model, data):
    logs = {k: log(data[k] / model[k]) for k in data}
    log_s = sum(logs.values()) / len(logs)
    return {k: exp(log_s - v) - 1 for k, v in logs.items()}  # s*model/measured - 1

def print_ranking(model, tests=None):
    width = max(len(" ".join(k)) for k in model)
    measured_rank = {}
    if tests:
        by_value = sorted(tests, key=tests.get, reverse=True)
        measured_rank = {combo: r for r, combo in enumerate(by_value, start=1)}

    for rank, (combo, value) in enumerate(model.items(), start=1):
        label = " ".join(combo)
        line = f"{rank:>2}. {label:<{width}}  {value:7.3f}"
        if combo in measured_rank:
            line += f"  measured {tests[combo]:6.1f} ({measured_rank[combo]})"
        print(line)

if __name__ == "__main__":
    run = load_run("Data/set_1.json")
    model = find_max(run["base_constants"], run["steps"])
    errs = relative_errors(model, run["data"])

    for k, e in sorted(errs.items(), key=lambda kv: abs(kv[1]), reverse=True):
        print(f"{k}: {e:+.2%}")

    vals = list(errs.values())
    n = len(vals)

    print(f"\nMean absolute error:     {sum(abs(e) for e in vals) / n:.2%}")
    print(f"Root mean squared error: {(sum(e * e for e in vals) / n) ** 0.5:.2%}")
    print(f"Max error:               {max(abs(e) for e in vals):.2%}")

    print("--------------------")
    print(f"Number of data: {len(run["data"])}, Number of combinations: {len(iterate_combinations())}")
    print("Ranking:")
    print_ranking(find_max(run["base_constants"], run["steps"]), run["data"])