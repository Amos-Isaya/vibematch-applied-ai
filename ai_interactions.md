# Workflow trace

The recommendation workflow validates the listener's input, retrieves matching songs, applies the energy guardrail, ranks the survivors, and returns recommendations or an empty result. Its saved operational trace records the actual plan, candidate and rejection counts, and returned titles; it does not claim to expose hidden model reasoning.

Reproduce the committed trace:

```bash
python -m src.main --genre lofi --mood chill --energy 0.4 --count 1 --trace logs/lofi_trace.txt
```

[View the committed trace](logs/lofi_trace.txt). The trace contains the provided preferences; avoid saving sensitive information in public logs.
