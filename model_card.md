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

## AI collaboration and reflection

I collaborated with Codex to extend my Module 3 recommender. Codex inspected the original project, built the retrieval and verification workflow, and helped document and test it. I used the original project's high-energy lofi experiment as a concrete case for checking whether the new system addressed the problem.

I accepted the suggestion to verify the energy gap before ranking: the original scoring could favor songs that matched the genre and mood but were much less energetic than requested. Adding a separate energy check makes that conflict visible, including when no candidate passes.

I revised the approach by keeping the workflow bounded and rule-based instead of adding an external language model. This simplified setup and made the decision steps reproducible without an API key. The trade-off is that it cannot interpret nuanced natural-language preferences or learn a listener's taste. The six tests check specific behaviors; they cannot show that real listeners will enjoy the results or that the catalog represents them fairly.
