# Future Radio Sound Cues

Deterministic prototype cue assets for Future Radio Sound Bible v1. These are symbolic, editable source cues for local assembly, not a finished score and not evidence of consent, publication, funding, or achievement.

## Contents

- `cues/fr-carrier.wav` — FR-CARRIER, station connection only
- `cues/fr-packet.wav` — FR-PACKET, composite four-bar message
- `cues/fr-agnolo-isolation.wav` — dry percussion/counting interpretation
- `cues/fr-borges-isolation.wav` — returning two-note string figure
- `cues/fr-leonardo-isolation.wav` — ascending unresolved breath phrase
- `cues/fr-record.wav` — FR-RECORD, preserved object cue
- `cues/fr-open.wav` — FR-OPEN, suspended incomplete-work cue
- `cues/fr-eval.wav` — FR-EVAL, post-curtain pencil and tone
- `cues/fr-assemble.wav` — FR-ASSEMBLE, edit-click prototype

All WAVs are mono, 48 kHz, 16-bit PCM. The packet and its three foreground stems use the same deterministic seed (`120026`) and duration so they can be compared and recombined.

## ArtRiver assessment

This repository is intentionally compatible with ArtRiver's local-first model: the WAVs, generator, manifest, and later mix/project states can be tracked as an ArtRiver project. ArtRiver is currently a local prototype with `arp session`, `arp revise`, `arp flow`, `arp runoff`, `arp checkout`, and `arp diff`; its remote Glacier/Iceberg concepts are not production-ready. GitHub is the public distribution mirror for this first pass. Do not treat a GitHub commit as an ArtRiver signed patch or a public release receipt.

Suggested ArtRiver workflow when the CLI is installed:

```sh
arp session .
arp revise cues manifests generate_cues.py
arp flow -m "Seeded Future Radio cue prototypes"
arp runoff packet-variant
# edit/regenerate in the runoff, then compare and preserve deliberately
arp diff main packet-variant
```

## Provenance

- Source specification: Future Radio Sound Bible v1, supplied locally by Leo.
- Generator: `generate_cues.py`.
- Manifest: `manifests/cue-manifest.json`.
- Seed: `120026`.
- Generated locally; no external music-generation API was used for these cue prototypes.
