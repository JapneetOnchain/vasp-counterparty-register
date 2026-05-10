# VASP Counterparty Risk Register

A reproducible assessment framework for compliance teams evaluating crypto VASP counterparty exposure.

## What this is

This toolkit provides a structured methodology for assessing crypto Virtual Asset Service Providers (VASPs) across seven compliance-relevant dimensions. It combines researched regulatory data with live on-chain measurements, packaged for use by compliance professionals, consultants, and researchers.

The framework currently covers 10 entities spanning four counterparty categories: centralized exchanges, stablecoin issuers, custodians, and decentralized protocol infrastructure.

## Three ways to use this

**Live web app** (recommended for non-technical users):
[Streamlit URL — to be added]

**Live on-chain dashboard** (for empirical verification):
[https://dune.com/japneet/vasp-counterparty-register](https://dune.com/japneet/vasp-counterparty-register)

**Source code and data** (for technical users and forking):
This GitHub repository

## What's in this repository

- `entities/` — JSON files containing the assessment data for each entity (10 files, one per entity)
- `rubric/` — The scoring rubric in YAML format
- `src/` — The Python toolkit that reads entity data and produces assessments
- `dune/` — The SQL queries that power the on-chain layer
- `examples/` — Sample assessment outputs
- `METHODOLOGY.md` — Full framework documentation
- `LIMITATIONS.md` — Explicit acknowledgment of what this tool does NOT do

## The seven dimensions

1. Licensing and Regulatory Standing
2. Travel Rule Operational Compliance
3. Sanctions and Enforcement History
4. Stablecoin Reserve Transparency (applicable only to issuers)
5. On-Chain Exposure (5A: sanctioned addresses; 5B: mixer infrastructure)
6. KYC/CDD Posture
7. Operational Track Record

Each dimension uses categorical scoring with explicit sourcing. Scores are not weighted into a single composite; users can apply their own weighting based on their specific risk priorities.

## Notable empirical finding

Across 10 major centralized exchanges measured (Coinbase, Binance, Kraken, OKX, Bybit, Bitget, MEXC, Gate.io, KuCoin, HTX), zero direct on-chain transfers to Tornado Cash ETH pools were observed in the 12-month measurement window ending April 2026. During the same window, the four primary Tornado Cash ETH pools received approximately 4,029 ETH in deposits from non-exchange-attributed sources.

The empirical pattern suggests that direct exchange-to-mixer flow is not the operational compliance signal worth monitoring. The relevant pattern is intermediated flows through unattributed wallets, which require multi-hop tracing tools beyond the scope of public address attribution.

Full methodology and limitations documented in METHODOLOGY.md.

## Who built this

Japneet Singh - Crypto native TradFi AML professional with five years of experience across EY (forensic investigations), KPMG (AML remediation), American Express (KYC/AML onboarding for EU and APAC markets), and National Australia Bank (transaction monitoring with crypto-asset exposure). Currently working on the bridge between TradFi compliance discipline and on-chain technical capability.

This is part of an ongoing publishing portfolio of original on-chain forensic investigations and compliance frameworks. Previous work covers exploits at Drift Protocol, Resolv, and CoW Protocol.

GitHub: [JapneetOnchain](https://github.com/JapneetOnchain)

## Status

Version 0.1 (May 2026). Initial release with 10-entity vertical slice across all 7 dimensions. Future versions will extend to additional entities and additional on-chain dimensions.

This toolkit is open source, free to use, fork, and extend.

## What this is NOT

- Not a replacement for licensed analytics providers (Chainalysis, TRM, Elliptic, Crystal Intelligence)
- Not enterprise software with SLAs or support
- Not legal or regulatory advice
- Not a complete compliance program — it is one input to one decision (counterparty selection)

See LIMITATIONS.md for full acknowledgment of methodology constraints.