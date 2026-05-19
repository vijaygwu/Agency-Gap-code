# Companion code for "The Agency Gap"

This directory holds the small, illustrative scripts referenced from Appendix B and the in-text sidebars. The book's claims are not built on this code; this code shows you the math from Chapter 5's sidebars and the framework from Chapter 2.

If you are reproducing a finding from one of the chapters, the source paper (listed in Appendix A) is the authoritative reference. The scripts here are checks on the math and templates you can copy into your own infrastructure.

## What's here

| File | Companion to | What it does |
|---|---|---|
| `beta_gating_sanity_check.py` | Chapter 5 §5.4 sidebar; Appendix B.2 | Contrasts naive empirical-accuracy gating against LiSA's Beta-posterior lower-bound gating under simulated label noise. Runs on CPU in under a minute. |
| `four_property_test.py` | Chapter 2 §2.2 | CLI that asks four yes/no questions about a candidate system and prints a verdict (agent / workflow / pipeline). Pedagogical. |
| `champion_challenger_template.yaml` | Chapter 10 §10.4; Appendix B.3 | Minimal champion-challenger eval config with inline `# why` comments. Copy and adapt; do not deploy as-is. |
| `requirements.txt` | All | Two dependencies: `numpy`, `scipy`. Python 3.10+. |

## Quickstart

```bash
cd book-4/code
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python beta_gating_sanity_check.py
python four_property_test.py
```

Expected `beta_gating_sanity_check.py` output (deterministic with seed=42):

```
Naive accuracy gate: admit=57.50%, false-admit=5.50%
Beta lower-bound gate: admit=21.50%, false-admit=0.00%
```

The Beta gate admits fewer items but admits the *right* ones; the pessimism in the lower bound is what makes the system robust to bad labels under sparse evidence.

## What's NOT here

- Full reproductions of SDAR, LiSA, or any of the other 2026 papers. Those require the original authors' codebases and substantial GPU time. The Appendix B claim-to-source map points to where each chapter's specific claims live in the source papers.
- Production-grade error handling, monitoring, or deployment harnesses. The runbooks in Chapters 5, 7, 8, and 10 carry the operational load; this code is illustrative.
- Anything in TypeScript, Rust, or another language. The book is Python-first.

## License

Same as the rest of the book repository.
