# Model card: VibeMatch verified recommender

## Intended use and method

A classroom demonstration of a deterministic recommendation agent over 18 fictional songs, not a real music service. It retrieves songs with an exact genre or mood match, filters on energy, then applies the Module 3 weighted scorer. The user reviews each result and may revise the request. There is no generative model, trained predictor, or probability of enjoyment.

## Limitations and biases

The fictional catalog is small and uneven across genres; its attributes are simulated, not measured audio. Exact labels miss related genres and moods. Fixed weights prioritize genre, while the 0.25 energy threshold can reject songs a person would enjoy. These design choices could underrepresent tastes poorly covered by the catalog. The results have not been tested with users.

## Misuse and mitigations

A user could mistake fictional songs for real releases or present scores as proven listener preferences. The CLI labels scores as rule-based, the documentation identifies the simulated catalog, and explanations show the matching rules. These measures do not prevent someone from copying results without context; do not use them for consequential profiling or claims about actual listeners.

## Reliability testing and surprise

| Check | Result | Meaning |
| --- | --- | --- |
| Six automated agent tests | 6 passed | Selected validation, ranking, and guardrail behaviors worked on the fixed test catalog. |
| High-energy chill lofi (0.95) | 4 retrieved, 4 rejected | The original genre-first ranking could prefer low-energy lofi; the hard constraint now produces no match. |
| Unknown genre and mood | No results | The agent does not fill a list with unrelated energy-only matches. |

The high-energy case illustrates a surprising trade-off: preventing the original mismatch can leave the listener with no suggestions. Passing tests does not measure enjoyment or establish fairness.

## AI collaboration — author review required

Codex inspected the prior repository, proposed and implemented the verification workflow, and ran the tests reported here. The author should replace this note with their own account of one AI suggestion they accepted and one they rejected or revised, including why. Those personal decisions cannot be inferred from the automated work and should not be fabricated.
