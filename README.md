# VASP Counterparty Risk Register

A reproducible 7-dimension counterparty risk assessment toolkit for crypto VASPs. Combines structured regulatory data with on-chain measurement, configurable risk weighting, and exportable compliance memos.

## 🔗 Three ways to use this

**🖥️ Live web app:** [https://vasp-counterparty-japneet.streamlit.app](https://vasp-counterparty-japneet.streamlit.app)
Configure your firm's risk priorities, generate decision recommendations, and export compliance memos.

**📊 Live on-chain dashboard:** [https://dune.com/japneet/vasp-counterparty-register](https://dune.com/japneet/vasp-counterparty-register)
Real-time on-chain exposure measurement against Tornado Cash mixer pools and OFAC SDN crypto addresses.

**💻 Source code:** This repository (forkable, MIT-licensed)

---

## What this is

A structured assessment framework covering 10 entities across four counterparty categories — centralized exchanges, stablecoin issuers, custodians, and decentralized protocol infrastructure — measured across 7 compliance-relevant dimensions:

1. **Licensing and Regulatory Standing**
2. **Travel Rule Operational Compliance**
3. **Sanctions and Enforcement History**
4. **Stablecoin Reserve Transparency** (issuers only)
5. **On-Chain Exposure** — 5A: sanctioned addresses; 5B: mixer infrastructure
6. **KYC/CDD Posture**
7. **Operational Track Record**

Each dimension uses categorical scoring with explicit sourcing, applied programmatically by the toolkit. Users configure their own dimension weights and the tool produces a weighted score, decision recommendation, and exportable compliance memo.

## Notable empirical finding

Across 10 major centralized exchanges (Coinbase, Binance, Kraken, OKX, Bybit, Bitget, MEXC, Gate.io, KuCoin, HTX), zero direct on-chain transfers to Tornado Cash ETH pools were observed in the 12-month measurement window ending April 2026. During the same window, the four primary Tornado Cash ETH pools received approximately 4,029 ETH in deposits from non-exchange-attributed sources.

The pattern suggests direct exchange-to-mixer flow is not the operational compliance signal worth monitoring at major centralized exchanges. The relevant pattern is intermediated flows through unattributed wallets, which require multi-hop tracing tools beyond the scope of public address attribution.

## Repository structure

- `entities/` — JSON files containing assessment data for 10 entities
- `src/assess.py` — Python toolkit reading entity data and producing assessments
- `src/app.py` — Streamlit web application
- `dune/` — SQL queries powering the on-chain dashboard
- `METHODOLOGY.md` — Full framework documentation

## Decision logic

The web app applies three layers of decision logic:

1. **Hard blockers** — Structural impossibilities (no licensing, no KYC, decentralized protocols) trigger automatic DECLINE
2. **Weighted scoring** — User-configurable weights produce a 0-10 score per entity
3. **Threshold mapping** — Score ≥ 8.0: APPROVE; 6.0-8.0: APPROVE WITH CONDITIONS; below 6.0: DECLINE

Output is a defensible compliance memo (markdown format) for risk committee review.

## Status

Version 0.1 (May 2026). Initial release with 10-entity vertical slice across all 7 dimensions. Future versions will extend to additional entities and additional on-chain dimensions.

## What this is NOT

- Not a replacement for licensed analytics providers (Chainalysis, TRM, Elliptic, Crystal Intelligence)
- Not enterprise software with SLAs or support
- Not legal or regulatory advice

See METHODOLOGY.md for full acknowledgment of methodology constraints.

## Author

**Japneet Singh**
Crypto compliance & on-chain forensics
[github.com/JapneetOnchain](https://github.com/JapneetOnchain)

Previous case studies: Drift Protocol governance takeover (Solana), Resolv USR exploit (EVM), CoW Protocol solver failure (EVM).