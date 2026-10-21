# Security Policy

## Reporting a vulnerability

This is a font file (`.otf` / `.ufo` source). Security vulnerabilities
are unlikely, but if you find one (e.g., a malicious glyph table,
font-table exploitation, supply-chain concern in the build pipeline),
email **security@jordannewell.com**.

Do not open a public GitHub issue for security reports.

If you have a PGP key, encrypt your report. GPG fingerprint of the project's
reporting key:

```
67567DC5E7C5353F85F2AF0DAC05D3F3E0EFA32A
```

## Response timeline

- **Acknowledgment:** within 72 hours
- **Initial assessment:** within 5 business days
- **Fix or mitigation:** target 30 days

## Scope

**In scope:**

- The compiled font binaries (`.otf`)
- The UFO source
- The build pipeline (fontTools / fontMake invocations)
- Release artifacts attached to GitHub releases

**Out of scope:**

- Rendering behavior in any specific application (browser, OS, design
  tool) — those are application bugs, not font bugs