# Companion code for *Engineering AI Agents*

Small, runnable companions for the book ***Engineering AI Agents: The Agency Gap After the Benchmarks Fell*** by Dr. Vijay Raghavan (Agentic AI Series, 2026).

These are illustrative scripts referenced from Chapter 2, Chapter 5, Chapter 10, and Appendix B. The book's claims rest on the source papers listed in Appendix A; this code shows you the math and gives you templates you can copy into your own infrastructure.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What's here

| File | Companion to | What it does |
|---|---|---|
| [`beta_gating_sanity_check.py`](beta_gating_sanity_check.py) | Chapter 5 §5.4 sidebar; Appendix B.2 | Contrasts naive empirical-accuracy gating against LiSA's Beta-posterior lower-bound gating under simulated label noise. CPU, under one minute. |
| [`four_property_test.py`](four_property_test.py) | Chapter 2 §2.2 | CLI that asks four yes/no questions about a candidate system and prints a verdict (agent / workflow / pipeline). Pedagogical. |
| [`champion_challenger_template.yaml`](champion_challenger_template.yaml) | Chapter 10 §10.4; Appendix B.3 | Minimal champion-challenger eval config with inline `# why` comments. Copy and adapt; do not deploy as-is. |
| [`tests/test_four_property.py`](tests/test_four_property.py) | — | Pytest suite for `four_property_test.classify()`. 3 tests, all green. |
| [`requirements.txt`](requirements.txt) | All | Two dependencies: `numpy`, `scipy`. Python 3.10+. |

## Quickstart

```bash
git clone https://github.com/vijaygwu/Agency-Gap-code.git
cd Agency-Gap-code

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python beta_gating_sanity_check.py
python four_property_test.py
pytest tests/
```

Expected `beta_gating_sanity_check.py` output (deterministic, seed=42):

```
Naive accuracy gate: admit=57.50%, false-admit=9.57%
Beta lower-bound gate: admit=21.50%, false-admit=0.00%
```

The Beta gate admits fewer items but admits the *right* ones; the pessimism in the lower bound is what makes the system robust to bad labels under sparse evidence. Chapter 5 §5.4 of the book unpacks why this matters in production memory and guardrail systems.

## What's *not* here

- Full reproductions of SDAR, LiSA, or any of the other 2026 papers the book draws on. Those require the original authors' codebases and substantial GPU time. The book's Appendix B claim-to-source map points to where each chapter's specific claims live in the source papers.
- Production-grade error handling, monitoring, or deployment harnesses. The runbooks in Chapters 5, 7, 8, and 10 carry the operational load; this code is illustrative.
- Anything in TypeScript, Rust, or another language. The book is Python-first.

## About the book

*Engineering AI Agents* is the fourth book in the Agentic AI Series. It argues that frontier AI's capability ceiling has fallen but the agency ceiling has not, and walks through the four open problems that remain: memory, coordination, deployment-time learning, and governance under autonomy. About 108,000 words, 404 pages, 10 chapters plus appendices.

- **Author:** Dr. Vijay Raghavan
- **Contact:** vijayrag@gwu.edu
- **Other repos in the series:** [github.com/vijaygwu](https://github.com/vijaygwu)

## License

MIT — see [LICENSE](LICENSE). Use, modify, and distribute freely.
