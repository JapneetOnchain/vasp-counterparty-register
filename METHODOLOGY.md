# Methodology — VASP Counterparty Risk Register

## 1. Framework Overview

### The problem this addresses

Traditional financial compliance teams encountering crypto counterparty exposure face a structural problem: existing assessment frameworks are either built for traditional banks (and don't address crypto-specific risks) or built for crypto-native firms (and assume operational fluency the TradFi team doesn't have).

This framework provides a baseline counterparty assessment structure designed for compliance teams that need bank-grade rigor without bank-scale resources. It is deliberately lean and tech-driven, reflecting the operational reality of compliance teams at fintechs, smaller exchanges, and TradFi institutions adding crypto exposure.

### Who this is for

- Compliance officers at TradFi institutions (banks, payment companies, asset managers) evaluating crypto counterparty exposure
- Compliance teams at fintech and crypto-native firms managing partner risk
- Compliance consultants providing counterparty due diligence services
- Researchers and journalists studying the crypto compliance landscape
- Hiring managers evaluating crypto compliance candidate work

### What this framework deliberately is NOT

- **Not a replacement for licensed analytics providers.** Chainalysis, TRM Labs, Elliptic, and Crystal Intelligence provide capabilities that this framework explicitly does not — proprietary attribution, multi-hop tracing, threat intelligence integration, real-time monitoring at scale. This framework provides a structured public-data baseline. Licensed analytics provide the depth.
- **Not enterprise software.** No SLAs, no support, no production guarantees. A high-quality reference implementation packaged for use.
- **Not legal or regulatory advice.** Compliance decisions should be made by qualified compliance professionals with knowledge of the specific regulatory context.
- **Not a complete compliance program.** Counterparty assessment is one input among many. This framework addresses that one input well; other compliance program components (transaction monitoring, sanctions screening, customer due diligence on direct customers) are out of scope.

## 2. The Seven Dimensions

### Dimension 1: Licensing and Regulatory Standing

**What this measures:** The breadth and depth of regulatory authorization across major jurisdictions. Captures whether the entity holds licenses appropriate to its operational footprint and whether those licenses come from credible regulators.

**Categorical scoring:**
- Comprehensive multi-jurisdiction
- Significant single-jurisdiction
- Limited or partial
- No identifiable major-jurisdiction authorization
- Authorization revoked or suspended

**Sourcing standards:** Primary sources are the regulator's own published license registers, the entity's official disclosure pages, and reputable news reporting on license issuance/revocation.

**Known limitations:** A license issued does not guarantee a license actively supervised. Some jurisdictions issue licenses with light ongoing supervision (a concern raised in 2025 ESMA peer reviews of Malta's MiCA authorizations, for example). The framework captures the formal license status; users may want to apply additional weighting based on the supervising regulator's reputation.

### Dimension 2: Travel Rule Operational Compliance

**What this measures:** Operational implementation of FATF Recommendation 16 (the Travel Rule) — the requirement that VASPs transmit originator and beneficiary information for crypto transfers above defined thresholds.

**Categorical scoring:**
- Comprehensive disclosed compliance
- Disclosed compliance with applicable regimes
- Limited disclosed compliance
- Not applicable (e.g., issuers, decentralized protocols)

**Sourcing standards:** TRUST consortium membership (the closed-network solution adopted by major regulated VASPs), public statements on Travel Rule technology vendor partnerships (Notabene, Sumsub, etc.), and disclosed jurisdictional Travel Rule compliance.

**Known limitations:** Travel Rule compliance is less publicly disclosed than licensing. Companies do not generally issue press releases about Travel Rule technology selections. The TRUST consortium membership signal is doing significant work as a publicly-verifiable indicator. Sunrise issue (variable enforcement timing across jurisdictions) creates compliance ambiguity that this framework cannot fully resolve.

### Dimension 3: Sanctions and Enforcement History

**What this measures:** Historical regulatory enforcement actions, settlements, criminal pleas, civil penalties, and ongoing compliance monitorships.

**Categorical scoring:**
- No material enforcement
- Material enforcement, resolved
- Material enforcement, partially resolved
- Severe enforcement, resolved with ongoing constraints
- Severe enforcement, ongoing monitorship

**Sourcing standards:** Primary sources are regulator press releases, court documents, and consent orders. Secondary sources include reputable industry reporting.

**Known limitations:** Enforcement history is one signal among many. Past enforcement does not necessarily predict future risk; entities under active monitorship are paradoxically often the most closely supervised. Conversely, no enforcement history may reflect either strong compliance or low regulatory attention.

### Dimension 4: Stablecoin Reserve Transparency

**What this measures:** For stablecoin issuers, the comprehensiveness of reserve disclosure including composition, custodians, attestation cadence, audit status, and regulatory framework alignment.

**Categorical scoring:**
- Comprehensive transparency
- Adequate transparency
- Limited but improving transparency
- Limited transparency
- Not applicable (non-issuers)

**Sourcing standards:** Issuer transparency pages, third-party attestation reports (Big Four preferred over smaller firms), full audit documents (where available), regulatory compliance filings.

**Known limitations:** Attestations are not full audits and have meaningfully weaker assurance. Reserve quality at a point in time does not guarantee reserve quality across all time periods. Custodian disclosure varies in granularity.

### Dimension 5A: On-Chain Exposure to Currently-Sanctioned Addresses

**What this measures:** Direct (1-hop) on-chain transfers between the entity's publicly-labeled addresses and crypto addresses currently on the OFAC SDN list.

**Reference Set:** OFAC SDN crypto address list, extracted via the 0xB10C/ofac-sanctioned-digital-currency-addresses GitHub repository. Includes ETH and Tron addresses currently sanctioned. Excludes Tornado Cash smart contracts (delisted March 21, 2025; measured separately under 5B as recognized mixer infrastructure regardless of current sanctions status).

**Categorical scoring:**
- Negligible exposure
- Limited exposure
- Material exposure
- Insufficient public attribution (data gap)
- Not applicable (issuers, protocols)

**Sourcing standards:** Direct on-chain measurement via Dune Analytics queries against `ethereum.transactions` joined with `labels.addresses` for entity attribution.

**Known limitations:**
- Bitcoin sanctioned addresses out of scope (Dune coverage limitation)
- Public address attribution sets are community-curated and incomplete
- For exchanges with rotating address infrastructure, currently-active addresses are typically a small subset of total labeled addresses
- 1-hop direct measurement does not capture multi-hop laundering through intermediary wallets

### Dimension 5B: On-Chain Exposure to Mixer Infrastructure

**What this measures:** Direct (1-hop) on-chain transfers between the entity's publicly-labeled addresses and recognized mixer infrastructure (specifically the four primary Tornado Cash ETH pools).

**Reference Set:** The four Tornado Cash ETH pool contracts on Ethereum mainnet:
- 0.1 ETH pool: `0x12d66f87a04a9e220743712ce6d9bb1b5616b8fc`
- 1 ETH pool: `0x47ce0c6ed5b0ce3d3a51fdb1c52dc66a7c3c2936`
- 10 ETH pool: `0x910cbd523d972eb0a6f4cae4618ad62622b39dbf`
- 100 ETH pool: `0xA160cdAB225685dA1d56aa342Ad8841c3b53f291`

These contracts were OFAC-sanctioned in August 2022 and officially delisted from the SDN list in March 2025 (per Van Loon v. Treasury). They remain the most recognized mixer infrastructure on Ethereum and are measured here regardless of current sanctions status, consistent with FATF mixer guidance.

**Categorical scoring:** Same as 5A.

**Empirical finding:** Across 10 major exchanges measured (Coinbase, Binance, Kraken, OKX, Bybit, Bitget, MEXC, Gate.io, KuCoin, HTX), zero direct on-chain transfers to Tornado Cash ETH pools were observed in the 12-month measurement window ending April 2026. During the same window, the four pools received approximately 4,029 ETH in deposits from non-exchange-attributed sources.

The empirical pattern suggests that direct exchange-to-mixer flow is not the operational compliance signal worth monitoring at major centralized exchanges. The relevant pattern is intermediated flows through unattributed wallets, which require multi-hop tracing tools beyond the scope of public address attribution.

### Dimension 6: KYC/CDD Posture

**What this measures:** The disclosed comprehensiveness of the entity's KYC and customer due diligence program — tier structure, jurisdictional scope, enhanced due diligence policies, sanctions and PEP screening, and historical regulatory findings on program adequacy.

**Categorical scoring:**
- Comprehensive disclosed program
- Disclosed program with historical concerns
- Recently strengthened program after enforcement
- Limited public KYC framework disclosure
- Issuer KYC framework (institutional-only, retail at exchange layer)
- No KYC by design (decentralized protocols)

**Sourcing standards:** Public compliance disclosures, regulatory consent orders citing KYC/CDD deficiencies, public statements on KYC vendor partnerships.

**Known limitations:** Disclosed program comprehensiveness is not the same as operational program effectiveness. Entities with strong public disclosure may have implementation gaps; entities with limited public disclosure may have strong operational programs. The dimension captures what is publicly verifiable.

### Dimension 7: Operational Track Record

**What this measures:** Operating history, hack/exploit incidents and recovery, leadership stability, and (for listed entities) public market scrutiny.

**Categorical scoring:**
- Strong long-term track record
- Strong track record with one significant stress event
- Mixed track record
- Material historical incidents, current stability
- Material historical concerns, ongoing scrutiny

**Sourcing standards:** Corporate disclosures, SEC filings (for listed entities), public incident reporting.

**Known limitations:** Past operational performance does not guarantee future performance. Incidents from earlier in an entity's history may have been addressed by current architecture and leadership.

## 3. Entity Selection

The current 10-entity slice was chosen to span the four major counterparty categories any TradFi or fintech compliance team would assess when contemplating crypto-asset exposure:

**Centralized exchanges (4):** Coinbase, Binance, Kraken, OKX. Selected for their global scale, regulatory significance across multiple jurisdictions, and varied enforcement profiles (from Coinbase's NYDFS-licensed posture to OKX's 2025 DOJ settlement).

**Stablecoin issuers (3):** Circle, Paxos, Tether. Selected for the contrast in regulatory transparency (Circle's MiCA-and-OCC posture vs. Paxos's NYDFS-and-OCC posture vs. Tether's El Salvador-only posture).

**Custodians (2):** Anchorage Digital, BitGo. Selected as the two most prominent federally-supervised crypto custodians (Anchorage's pre-existing OCC charter vs. BitGo's December 2025 conditional approval).

**Decentralized protocol infrastructure (1):** Tornado Cash protocol.

### Why Tornado Cash is included

Tornado Cash is included as a contrast/calibration entity, NOT as a counterparty a TradFi or fintech compliance program would consider transacting with directly. Its inclusion serves two purposes:

1. It provides a reference point for the on-chain dimensions (5B specifically). The protocol contracts are the reference set against which exchange exposure is measured.

2. It demonstrates the framework's applicability to non-VASP infrastructure. The framework's categorical scoring system extends naturally to entities for which traditional compliance categories (licensing, KYC) are structurally not applicable.

## 4. On-Chain Methodology

### Query architecture

All on-chain measurements use Dune Analytics queries against `ethereum.transactions` joined with `labels.addresses` for entity attribution. The queries are public and forkable; URLs are accessible via the Dune dashboard.

The query pattern is consistent across both 5A (sanctioned addresses) and 5B (mixer infrastructure):

1. Identify the reference set (sanctioned addresses or mixer pool contracts)
2. Identify the entity's publicly-labeled addresses
3. Measure direct (1-hop) transfers in both directions over the 12-month window
4. Aggregate results

### Time window

12 months trailing from the query date. The trailing window balances recency (capturing current operational patterns) with sample size (one year of data is more robust than one month).

### Reference Sets

**Reference Set 1 — Currently sanctioned crypto addresses:**
Source: OFAC SDN list, extracted via 0xB10C/ofac-sanctioned-digital-currency-addresses GitHub repository.
Snapshot date: 2026-04-29.
Includes: ETH and Tron addresses currently on the SDN list, including the April 24, 2026 CBI Tron address additions and historical DPRK-attributed addresses.
Excludes: Tornado Cash smart contracts (delisted March 21, 2025; measured under 5B regardless).
Out of scope for current methodology: Bitcoin sanctioned addresses (Dune coverage limitation).

**Reference Set 2 — Mixer/privacy infrastructure:**
The four primary Tornado Cash ETH pool contracts on Ethereum mainnet (addresses listed above in Dimension 5B section).
Source: Etherscan-verified contract pages.
Inclusion rationale: These contracts are NOT currently OFAC-sanctioned (delisted March 21, 2025) but are measured as recognized mixer infrastructure regardless of current sanctions status, consistent with FATF mixer guidance and broader compliance industry practice.

## 5. Limitations

### Public address attribution

The framework relies on Dune Analytics's `labels.addresses` table for entity attribution. This is community-curated and has known limitations:

- For exchanges with rotating address infrastructure (regularly creating new deposit/withdrawal addresses and retiring old ones), the labeled set is a mix of currently-active and historically-active addresses. The active subset may be small.
- For institutional custodians (Anchorage, BitGo), public attribution coverage is sparse. The framework explicitly acknowledges these as data gaps rather than claiming negligible exposure findings that the data cannot support.
- Some exchanges may use addresses not present in the public attribution layer; flows through such addresses are invisible to this framework.

### 1-hop direct measurement

The framework measures direct (1-hop) on-chain transfers only. Sophisticated illicit fund flows typically involve multi-hop intermediation through unattributed wallets. The framework cannot detect such patterns.

This is the most consequential limitation. The empirical finding that direct exchange-to-mixer flows are essentially zero across major exchanges should NOT be interpreted as "major exchanges have no mixer exposure." It should be interpreted as "the relevant compliance signal lives in intermediated flows that this framework does not measure."

Multi-hop tracing requires licensed analytics tools (Chainalysis, TRM Labs, Elliptic, Crystal Intelligence) that maintain proprietary clustering models, attribution intelligence, and threat databases. These tools are recommended for compliance programs that need depth beyond this framework's baseline.

### 12-month window

The trailing 12-month window may miss longer-term trends. Entities with infrequent but large historical exposure events would not be captured if those events fell outside the window.

### Categorical scoring without composite weighting

The framework deliberately does not produce a single composite risk score. Reasoning:

1. Different compliance programs weight different dimensions differently. A US-based bank may weight Dimension 3 (US enforcement) heavily; an EU-based fintech may weight Dimension 1 (MiCA compliance) heavily.
2. Composite scores create false precision. Reducing seven dimensions to one number obscures the underlying pattern.
3. Categorical scores plus dimension-specific notes give compliance teams the information needed to make weighted judgments based on their specific risk priorities.

### Public information only

The framework uses only public information. Non-public intelligence (regulatory examination findings not made public, internal threat intelligence, private incident reporting) is not incorporated. Compliance teams with access to such information should layer it on top of this framework.

## 6. Reproducibility

All components of this framework are public and reproducible:

- All Dune queries are public and forkable on Dune Analytics
- All entity JSON data is in this GitHub repository
- All Python code is in this GitHub repository
- All sources cited are public URLs

Anyone can verify the methodology, modify the rubric, extend to additional entities, or fork the entire framework. The framework is open source and freely usable.

Updates to the framework will be reflected in versioned releases of this repository. Entity assessments will be re-verified periodically; the `last_verified` field in each entity JSON file indicates when the assessment was last reviewed against current public information.

## 7. About the Author

Japneet Singh is a financial crime compliance professional with five years of experience across forensic investigations, AML remediation, KYC/AML onboarding, and transaction monitoring with crypto-asset exposure. His career spans EY (forensic investigations and third-party due diligence including CBI forensic audit support), KPMG (AML remediation), American Express (KYC/AML onboarding for EU and APAC markets), and National Australia Bank (transaction monitoring with crypto-asset exposure).

His focus is on the bridge between TradFi compliance discipline and on-chain technical capability — the combination that institutional compliance programs increasingly require but few professionals genuinely embody.

This framework is part of an ongoing publishing portfolio of original on-chain forensic investigations and compliance methodology work. Previous case studies cover exploits at Drift Protocol, Resolv Protocol, and CoW Protocol. The portfolio is published at [github.com/JapneetOnchain](https://github.com/JapneetOnchain).

He is based in India and is currently exploring opportunities at crypto compliance firms, exchanges, stablecoin issuers, and consultancies. Direct contact via the GitHub profile.