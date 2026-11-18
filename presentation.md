# VibeMatch presentation script (approximately 5–7 minutes)

## 1. Problem and original project (about 1 minute)

My project is VibeMatch, a music recommendation simulation built in Python. It extends my Module 3 Music Recommender Simulation, which ranked 18 fictional songs by genre, mood, and energy. The original project gave a score and explanation for each song. During an earlier experiment, a listener asking for high-energy chill lofi still received low-energy songs because genre and mood had more weight than energy. I wanted the final system to make that trade-off clearer.

## 2. System architecture (about 1 minute)

Show `diagrams/architecture.mmd`. A listener supplies a genre, mood, and target energy. The program validates that input, retrieves songs matching the genre or mood, and rejects songs whose energy is more than 0.25 away from the requested value. It then uses the original scoring rules to rank the remaining candidates. Finally, it displays its reasons or tells the listener no songs passed. The listener is in the loop: they review the results and can change the request. This is a rule-based agent, not a language model or a trained prediction system.

## 3. Demo (about 2 minutes)

Run these commands from the project directory:

```bash
python -m src.main --genre lofi --mood chill --energy 0.4
python -m src.main --genre pop --mood happy --energy 0.9
python -m src.main --genre lofi --mood chill --energy 0.95
```

For the first two requests, show the ranked songs and explain that matching genre earns three points, matching mood earns two, and energy similarity contributes up to one. For the last request, point out that four candidates were retrieved but all four failed the energy guardrail, so the system asks the listener to revise the request rather than presenting them as verified matches. A score is a rule-based fit, not a probability of enjoyment.

## 4. Testing and responsible design (about 1–2 minutes)

Run `python -m unittest discover -s tests -p test_agent.py -v`. Explain that the six tests check a normal recommendation, energy rejection, no matches, invalid energy, invalid count, and input normalization. The catalog is small and fictional; exact matching and fixed weights can disadvantage genres with few examples. A strict energy constraint can also exclude songs someone might like. These tests check program behavior, not real-world recommendation quality or fairness.

## 5. Reflection and next steps (about 1 minute)

I collaborated with Codex to extend the original recommender, inspect its behavior, and build tests and documentation. I kept the proposed energy verification step because it addressed the mismatch in my earlier experiment. I also kept the workflow bounded and rule-based to make its decisions reproducible without an API key. One lesson is that verification can expose a conflict between preferences rather than hiding it behind a single score. A future improvement would be to test the threshold with real listeners and use a larger, more representative catalog.
