"""Beta-gating sanity check: contrasts a naive empirical-accuracy gate
against LiSA's Beta-posterior lower-bound gate under simulated label noise.

Runnable companion for Chapter 5 §5.4 and Appendix B.2 of "Engineering AI Agents."
Python 3.10+. Dependencies: numpy, scipy.

The check is qualitative: under noisy observations, the Beta lower-bound
gate admits substantially fewer items than naive accuracy at the same
threshold, but with a much lower false-admit rate. The pessimism is the
point.
"""
import argparse
import json
import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.stats import beta


def beta_lower_bound(
    successes: ArrayLike,
    failures: ArrayLike,
    delta: float = 0.05,
) -> NDArray[np.float64]:
    """Return the (delta * 100)th-quantile of Beta(1+s, 1+c), vectorized.

    Accepts scalars or numpy arrays; broadcasts via scipy.stats.beta.ppf.
    The +1 priors implement a uniform Beta(1, 1) prior so a zero-observation
    item starts at the mean of the prior, not at undefined. The lower
    quantile is LiSA's pessimistic point estimate of the true success
    probability given (s, c) observations (Kim et al., 2026).
    """
    s = np.asarray(successes)
    c = np.asarray(failures)
    return beta.ppf(delta, 1 + s, 1 + c)


def _positive_int(value: str) -> int:
    iv = int(value)
    if iv <= 0:
        raise argparse.ArgumentTypeError(f"must be > 0, got {iv}")
    return iv


def _unit_float(value: str) -> float:
    fv = float(value)
    if not 0.0 <= fv <= 1.0:
        raise argparse.ArgumentTypeError(f"must be in [0, 1], got {fv}")
    return fv


def _nonneg_float(value: str) -> float:
    fv = float(value)
    if fv < 0.0:
        raise argparse.ArgumentTypeError(f"must be >= 0, got {fv}")
    return fv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Beta-gating sanity check comparing a naive accuracy gate "
            "against LiSA's Beta-posterior lower-bound gate."
        )
    )
    parser.add_argument("--seed", type=int, default=42,
                        help="PRNG seed (default: 42).")
    parser.add_argument("--n-items", type=_positive_int, default=200,
                        help="Number of candidate rules to simulate.")
    parser.add_argument("--noise", type=_nonneg_float, default=0.2,
                        help="Std-dev of Gaussian noise added to true acc.")
    parser.add_argument("--threshold", type=_unit_float, default=0.55,
                        help="Gate threshold; LiSA paper default 0.55.")
    parser.add_argument("--trials", type=_positive_int, default=10,
                        help="Observations per rule used to derive s, c.")
    parser.add_argument("--json", action="store_true", default=False,
                        dest="json_output",
                        help="Emit a single-line JSON object on stdout "
                             "instead of human-readable text. Useful for "
                             "machine-parseable CI logs.")
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    rng = np.random.default_rng(seed=args.seed)
    n_items = args.n_items

    # Ground-truth reliability of each candidate rule. The gate does not see
    # this; we use it later only to compute false-admit rate.
    true_accuracy = rng.uniform(0.4, 0.95, size=n_items)

    noisy_accuracy = np.clip(
        true_accuracy + rng.normal(0.0, args.noise, size=n_items),
        a_min=0.0,
        a_max=1.0,
    )
    successes = (noisy_accuracy * args.trials).astype(int)
    failures = args.trials - successes  # args.trials > 0 by argparse validator

    naive_gate = successes / args.trials
    beta_gate = beta_lower_bound(successes, failures)

    threshold = args.threshold
    bad_rule = true_accuracy < threshold  # ground truth: what should be rejected

    def admit_rate(gate: NDArray[np.float64]) -> float:
        return float((gate >= threshold).mean())

    def false_admit_rate(gate: NDArray[np.float64]) -> float:
        admitted = gate >= threshold
        if not admitted.any():
            return 0.0
        return float((admitted & bad_rule).sum() / admitted.sum())

    naive_admit = admit_rate(naive_gate)
    naive_false_admit = false_admit_rate(naive_gate)
    beta_admit = admit_rate(beta_gate)
    beta_false_admit = false_admit_rate(beta_gate)

    if args.json_output:
        # Single-line JSON on stdout: parseable by CI tooling. Seed is
        # echoed so a failing run can be replayed deterministically.
        payload = {
            "seed": args.seed,
            "n_items": n_items,
            "noise": args.noise,
            "threshold": threshold,
            "trials": args.trials,
            "naive_gate": {
                "admit_rate": round(naive_admit, 4),
                "false_admit_rate": round(naive_false_admit, 4),
            },
            "beta_gate": {
                "admit_rate": round(beta_admit, 4),
                "false_admit_rate": round(beta_false_admit, 4),
            },
        }
        print(json.dumps(payload))
        return

    # Seed printed first so it appears even when the human-readable
    # output is captured in a log; lets practitioners replay a run.
    print(f"Seed: {args.seed}")
    print(f"Naive accuracy gate: admit={naive_admit:.2%}, "
          f"false-admit={naive_false_admit:.2%}")
    print(f"Beta lower-bound gate: admit={beta_admit:.2%}, "
          f"false-admit={beta_false_admit:.2%}")


if __name__ == "__main__":
    main(parse_args())
