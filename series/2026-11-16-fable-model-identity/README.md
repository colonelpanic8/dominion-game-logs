# Fable profile versus actual model: append-only correction

The original finished run records remain unchanged. Their agent profile is the requested configuration; it does not establish the model that generated every response.

In [g69](../../runs/2026-11-16/fable-astra-g69), the Fable-labelled Claude session emitted two `claude-fable-5-2` assistant messages, then 350 `claude-opus-5` assistant messages. Its final provider usage recorded 89 Fable output tokens and 116,600 Opus output tokens. The raw interaction and native stdout journals preserve this evidence. This match cannot be presented as a clean Fable-versus-Astra measurement.

The three Fable attempts in g70 each reported a provider refusal tagged `reasoning_extraction`; the error text named Opus 5. The user chose to exclude that technical forfeit from the series score and replay it once Fable is healthy. Its authoritative result and all traces remain preserved locally for the subsequent full-series archive.

The in-progress g71 session also emitted Opus messages after two Fable messages. A snapshot of these findings is in `findings.json`; it is not a final result or new score adjudication. The active game is left to finish, with further matches held.

The separate investigation traced the refusal/fallback sequence to playbook instructions demanding written reasoning. A revised playbook is being prepared to request a concise plan and game-fact explanations instead. It has not yet been validated with the requested Fable model. No provider substitution or safeguard bypass is authorized.
