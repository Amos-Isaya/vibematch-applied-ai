# VibeMatch: Verified Music Recommendations

VibeMatch helps a listener explore a small fictional music catalog using an explainable, rule-based recommendation agent. It retrieves relevant songs, checks an energy constraint, and ranks the remaining candidates. The listener reviews the results and can change their preferences; the program does not make decisions on their behalf.

## Original project

This extends [Module 3: Music Recommender Simulation](https://github.com/Amos-Isaya/ai110-module3show-musicrecommendersimulation-starter). The original VibeMatch ranked 18 fictional songs by genre, mood, and energy, displaying scores and explanations. Its weight experiments showed that a high-energy request could still rank much lower-energy songs first.

## Architecture and design

See the [Mermaid architecture source](diagrams/architecture.mmd). The bounded agent orchestrates four steps: validate preferences, retrieve songs matching genre or mood, reject candidates more than 0.25 energy units away, and use the original weighted scorer to rank and explain the survivors. If nothing passes, it asks the human to revise the request. This is a deterministic, rule-based agent; it does not call a language model or learn from listening history. Its score is a weighted fit, not a probability or a validated prediction of enjoyment.

The hard energy threshold addresses the original project's mismatch, but can exclude otherwise attractive songs. Exact labels and a tiny fictional catalog limit recall; candidates are not recommendations for real recordings. No personal preferences are stored, and the agent reports counts through Python logging when enabled.

## Setup and execution

Requires Python 3.9 or later; the application and new tests use only the standard library.

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m src.main --genre lofi --mood chill --energy 0.4
python -m unittest discover -s tests -p test_agent.py -v
```

To also run the original pytest tests, install `pytest` (`python -m pip install pytest`) and run `python -m pytest`. The original `requirements.txt` is retained for the earlier project and is not needed for the commands above. Energy must be a finite number from 0 to 1; `--count` is optional (1–10, default 3).

## Reproducible execution evidence

These are actual runs from the project directory:

```text
$ python3 -m src.main --genre lofi --mood chill --energy 0.4
Retrieved: 4 | Rejected by energy guardrail: 0
1. Midnight Coding — LoRoom | score 5.98 | energy 0.42
   Genre match (+3.0); Mood match (+2.0); Energy similarity (+0.98)
2. Library Rain — Paper Lanterns | score 5.95 | energy 0.35
   Genre match (+3.0); Mood match (+2.0); Energy similarity (+0.95)
3. Focus Flow — LoRoom | score 4.00 | energy 0.40
   Genre match (+3.0); Energy similarity (+1.00)
Scores are rule-based fit, not probabilities. Review the suggestions yourself.

$ python3 -m src.main --genre pop --mood happy --energy 0.9
Retrieved: 3 | Rejected by energy guardrail: 0
1. Sunrise City — Neon Echo | score 5.92 | energy 0.82
   Genre match (+3.0); Mood match (+2.0); Energy similarity (+0.92)
2. Gym Hero — Max Pulse | score 3.97 | energy 0.93
   Genre match (+3.0); Energy similarity (+0.97)
3. Rooftop Lights — Indigo Parade | score 2.86 | energy 0.76
   Mood match (+2.0); Energy similarity (+0.86)
Scores are rule-based fit, not probabilities. Review the suggestions yourself.

$ python3 -m src.main --genre lofi --mood chill --energy 0.95
Retrieved: 4 | Rejected by energy guardrail: 4
No verified matches. Try changing genre, mood, or energy.
Scores are rule-based fit, not probabilities. Review the suggestions yourself.
```

## Reliability and reflection

Six automated agent tests passed: ranking, energy rejection, no matches, invalid energy, invalid count, and case normalization/explanation. The high-energy lofi case now returns no match instead of a misleading low-energy song. This verifies selected rules on a fixed catalog; it does not establish user satisfaction, fairness, or accuracy in a real catalog. See [model_card.md](model_card.md) for risks, misuse, and AI collaboration.

The project illustrates how an explicit verification step can change an apparently plausible recommendation and make its trade-offs visible. A next step would be testing whether real listeners find the threshold useful before treating it as a preference.

## Presentation and portfolio

A [presentation outline](presentation.md) provides a 5–7 minute demo plan. The [portfolio entry](portfolio.md) links to the public repository and includes a reflection.
