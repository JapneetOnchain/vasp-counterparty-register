import json


def load_entity(entity_id):
    filepath = f"entities/{entity_id}.json"
    with open(filepath, "r") as f:
        data = json.load(f)
    return data


def assess_licensing(entity_data):
    licensing = entity_data["dimensions"]["dimension_1_licensing"]
    
    if not licensing["applicable"]:
        return {
            "dimension": "Licensing",
            "applicable": False,
            "flag": "N/A",
            "summary": "Not applicable for this entity type."
        }
    
    category = licensing["category"]
    
    if category == "Comprehensive multi-jurisdiction":
        flag = "PASS"
        analyst_note = "Strong regulatory standing across major jurisdictions. No material licensing concerns."
    elif category == "Significant single-jurisdiction":
        flag = "REVIEW"
        analyst_note = "Adequate licensing but concentrated in one jurisdiction. Consider concentration risk."
    elif category == "Limited or partial":
        flag = "FLAG"
        analyst_note = "Material gaps in major-jurisdiction authorization. Manual review required."
    elif category == "No identifiable major-jurisdiction authorization (by design)":
        flag = "FLAG"
        analyst_note = "Decentralized infrastructure with no licensing layer by design. Cannot be onboarded as regulated counterparty."
    else:
        flag = "REVIEW"
        analyst_note = f"Unknown category: '{category}'. Manual review required."
    
    return {
        "dimension": "Licensing",
        "applicable": True,
        "category": category,
        "flag": flag,
        "summary": licensing["summary"],
        "analyst_note": analyst_note,
        "sources": licensing["sources"]
    }


def assess_travel_rule(entity_data):
    travel_rule = entity_data["dimensions"]["dimension_2_travel_rule"]
    
    if not travel_rule["applicable"]:
        return {
            "dimension": "Travel Rule",
            "applicable": False,
            "flag": "N/A",
            "summary": "Not applicable for this entity type."
        }
    
    category = travel_rule["category"]
    
    if category == "Disclosed compliance with major regimes":
        flag = "PASS"
        analyst_note = "Strong publicly-verifiable Travel Rule compliance posture. TRUST consortium membership or equivalent institutional signal."
    elif category == "Disclosed compliance with applicable regimes":
        flag = "PASS"
        analyst_note = "Travel Rule compliance disclosed for jurisdictions where applicable. Verify coverage matches your transaction flows."
    elif category == "Limited disclosed compliance":
        flag = "REVIEW"
        analyst_note = "Limited public disclosure of Travel Rule operational compliance. Direct verification with counterparty recommended."
    elif category == "N/A as issuer; TRUST founding member":
        flag = "PASS"
        analyst_note = "Stablecoin issuer; Travel Rule applies to handling VASPs not issuer. TRUST membership demonstrates institutional commitment."
    elif category == "N/A — decentralized smart contract, no VASP":
        flag = "FLAG"
        analyst_note = "Decentralized protocol; cannot satisfy Travel Rule by design. Structural barrier to onboarding as regulated counterparty."
    else:
        flag = "REVIEW"
        analyst_note = f"Unknown category: '{category}'. Manual review required."
    
    return {
        "dimension": "Travel Rule",
        "applicable": True,
        "category": category,
        "flag": flag,
        "summary": travel_rule["summary"],
        "analyst_note": analyst_note,
        "sources": travel_rule.get("sources", [])
    }


def assess_sanctions_enforcement(entity_data):
    sanctions = entity_data["dimensions"]["dimension_3_sanctions_enforcement"]
    
    if not sanctions["applicable"]:
        return {
            "dimension": "Sanctions/Enforcement",
            "applicable": False,
            "flag": "N/A",
            "summary": "Not applicable for this entity type."
        }
    
    category = sanctions["category"]
    
    if category == "No material enforcement":
        flag = "PASS"
        analyst_note = "Clean enforcement record. No material regulatory actions."
    elif category == "Material enforcement, resolved":
        flag = "REVIEW"
        analyst_note = "Historical enforcement actions resolved. Review remediation evidence."
    elif category == "Material enforcement, partially resolved":
        flag = "REVIEW"
        analyst_note = "Some enforcement matters resolved; others ongoing. Detailed review required."
    elif category == "Severe enforcement, resolved with ongoing constraints":
        flag = "FLAG"
        analyst_note = "Severe historical enforcement; current operations under regulatory monitorship. Material counterparty risk consideration."
    elif category == "Severe enforcement, ongoing monitorship":
        flag = "FLAG"
        analyst_note = "Active regulatory monitorship in force. Heightened oversight; review monitor scope and duration."
    elif category == "Multiple historical enforcement actions, ongoing scrutiny":
        flag = "FLAG"
        analyst_note = "Pattern of recurring enforcement issues. Material counterparty risk; ongoing scrutiny suggests unresolved compliance posture."
    elif category == "Subject of major sanctions enforcement, partially reversed":
        flag = "FLAG"
        analyst_note = "Historical sanctions designation, currently delisted. Elevated risk indicator regardless of current status."
    else:
        flag = "REVIEW"
        analyst_note = f"Unknown category: '{category}'. Manual review required."
    
    return {
        "dimension": "Sanctions/Enforcement",
        "applicable": True,
        "category": category,
        "flag": flag,
        "summary": sanctions["summary"],
        "analyst_note": analyst_note,
        "sources": sanctions["sources"]
    }


def assess_reserve_transparency(entity_data):
    reserve = entity_data["dimensions"]["dimension_4_reserve_transparency"]
    
    if not reserve["applicable"]:
        return {
            "dimension": "Reserve Transparency",
            "applicable": False,
            "flag": "N/A",
            "summary": reserve.get("notes", "Not applicable — entity is not a stablecoin issuer.")
        }
    
    category = reserve["category"]
    
    if category == "Comprehensive transparency":
        flag = "PASS"
        analyst_note = "Reserve composition fully disclosed; multi-layer attestation cadence; G-SIB or equivalent custodians; aligned with major regulatory frameworks (MiCA, GENIUS Act, etc.)."
    elif category == "Adequate transparency":
        flag = "REVIEW"
        analyst_note = "Reasonable reserve disclosure but some gaps in cadence, custodian detail, or audit standards."
    elif category == "Limited but improving transparency":
        flag = "REVIEW"
        analyst_note = "Historical transparency gaps with active improvement signals (e.g., audit upgrades in progress). Current state remains weaker than peers; monitor improvement progress."
    elif category == "Limited transparency":
        flag = "FLAG"
        analyst_note = "Material gaps in reserve composition or attestation disclosure. Counterparty acceptance for institutional use cases not recommended without supplementary diligence."
    else:
        flag = "REVIEW"
        analyst_note = f"Unknown category: '{category}'. Manual review required."
    
    return {
        "dimension": "Reserve Transparency",
        "applicable": True,
        "category": category,
        "flag": flag,
        "summary": reserve["summary"],
        "analyst_note": analyst_note,
        "sources": reserve.get("sources", [])
    }


def assess_sanctioned_addresses(entity_data):
    sanctioned = entity_data["dimensions"]["dimension_5a_sanctioned_addresses"]
    
    if not sanctioned["applicable"]:
        return {
            "dimension": "Sanctioned Address Exposure",
            "applicable": False,
            "flag": "N/A",
            "summary": sanctioned.get("notes", "Not applicable for this entity type.")
        }
    
    category = sanctioned["category"]
    
    if category == "Negligible exposure":
        flag = "PASS"
        analyst_note = "Empirical measurement against current OFAC SDN crypto address set returned zero direct (1-hop) exposure. Note: 1-hop measurement does not capture multi-hop intermediated flows."
    elif category == "Limited exposure":
        flag = "REVIEW"
        analyst_note = "Some direct exposure to sanctioned addresses observed. Review specific instances and entity's response/freezing capability."
    elif category == "Material exposure":
        flag = "FLAG"
        analyst_note = "Material direct exposure to currently-sanctioned addresses. Significant counterparty risk; not recommended without enhanced due diligence."
    elif category == "Insufficient public attribution":
        flag = "REVIEW"
        analyst_note = "Public address attribution sparse for this entity type. Cannot produce defensible direct-exposure measurement; recommend licensed analytics tools for verification."
    elif category == "Notable exception — issuer-level mechanism":
        flag = "REVIEW"
        analyst_note = "Stablecoin issuer with on-chain freeze capability; assessment shifts from 'did entity transact with sanctioned addresses' to 'how responsively does issuer freeze flagged addresses.' Compare freeze response cadence to peers."
    else:
        flag = "REVIEW"
        analyst_note = f"Unknown category: '{category}'. Manual review required."
    
    return {
        "dimension": "Sanctioned Address Exposure",
        "applicable": True,
        "category": category,
        "flag": flag,
        "summary": sanctioned.get("summary", ""),
        "analyst_note": analyst_note,
        "sources": sanctioned.get("sources", [])
    }


def assess_mixer_exposure(entity_data):
    mixer = entity_data["dimensions"]["dimension_5b_mixer_exposure"]
    
    if not mixer["applicable"]:
        return {
            "dimension": "Mixer Exposure",
            "applicable": False,
            "flag": "N/A",
            "summary": mixer.get("notes", "Not applicable for this entity type.")
        }
    
    category = mixer["category"]
    
    if category == "Negligible exposure":
        flag = "PASS"
        analyst_note = "Empirical measurement against the four primary Tornado Cash ETH pools returned zero direct (1-hop) exposure across 12-month window. Note: this is a floor measurement at the publicly-attributable layer; multi-hop intermediation through unattributed wallets is the relevant compliance signal."
    elif category == "Limited exposure":
        flag = "REVIEW"
        analyst_note = "Some direct exposure to mixer infrastructure observed. Review specific instances."
    elif category == "Material exposure":
        flag = "FLAG"
        analyst_note = "Material direct exposure to mixer infrastructure. Significant counterparty risk indicator."
    elif category == "Insufficient public attribution":
        flag = "REVIEW"
        analyst_note = "Public address attribution sparse for this entity type. Cannot produce defensible direct-exposure measurement; recommend licensed analytics tools for verification."
    elif category == "IS the reference set — not measured against":
        flag = "FLAG"
        analyst_note = "Entity is the mixer infrastructure reference set itself. Empirically active: ~4,029 ETH in deposits to the four primary Tornado Cash ETH pools during the 12-month measurement window from non-exchange-attributed sources."
    else:
        flag = "REVIEW"
        analyst_note = f"Unknown category: '{category}'. Manual review required."
    
    return {
        "dimension": "Mixer Exposure",
        "applicable": True,
        "category": category,
        "flag": flag,
        "summary": mixer.get("summary", ""),
        "analyst_note": analyst_note,
        "sources": mixer.get("sources", [])
    }


def assess_kyc_cdd(entity_data):
    kyc = entity_data["dimensions"]["dimension_6_kyc_cdd"]
    
    if not kyc["applicable"]:
        return {
            "dimension": "KYC/CDD Posture",
            "applicable": False,
            "flag": "N/A",
            "summary": kyc.get("notes", "Not applicable for this entity type.")
        }
    
    category = kyc["category"]
    
    if category == "Comprehensive disclosed program":
        flag = "PASS"
        analyst_note = "Comprehensive publicly-disclosed KYC/CDD program. Mandatory at all account tiers; sanctions and PEP screening; ongoing transaction monitoring."
    elif category == "Disclosed program with historical concerns":
        flag = "REVIEW"
        analyst_note = "Current program is publicly disclosed but historical KYC/CDD deficiencies are documented in regulatory enforcement. Review remediation evidence and monitor scope."
    elif category == "Recently strengthened program after enforcement":
        flag = "REVIEW"
        analyst_note = "Recent enforcement specifically addressed KYC/AML deficiencies. Post-settlement program is materially stronger but recent; under regulatory monitorship."
    elif category == "Limited public KYC framework disclosure":
        flag = "FLAG"
        analyst_note = "Limited public disclosure of KYC procedures. Counterparty due diligence requires direct verification; institutional acceptance limited."
    elif category == "Issuer KYC framework (institutional only)":
        flag = "PASS"
        analyst_note = "Stablecoin issuer with institutional-only KYC framework. Retail KYC handled at exchange/distribution layer where the asset is acquired."
    elif category == "No KYC by design":
        flag = "FLAG"
        analyst_note = "Decentralized protocol with no KYC layer by design. Structurally incompatible with regulated counterparty status."
    else:
        flag = "REVIEW"
        analyst_note = f"Unknown category: '{category}'. Manual review required."
    
    return {
        "dimension": "KYC/CDD Posture",
        "applicable": True,
        "category": category,
        "flag": flag,
        "summary": kyc.get("summary", ""),
        "analyst_note": analyst_note,
        "sources": kyc.get("sources", [])
    }


def assess_operational_track_record(entity_data):
    track_record = entity_data["dimensions"]["dimension_7_operational_track_record"]
    
    if not track_record["applicable"]:
        return {
            "dimension": "Operational Track Record",
            "applicable": False,
            "flag": "N/A",
            "summary": track_record.get("notes", "Not applicable for this entity type.")
        }
    
    category = track_record["category"]
    
    if category == "Strong long-term track record":
        flag = "PASS"
        analyst_note = "Established operating history; clean incident record; stable leadership."
    elif category == "Strong track record":
        flag = "PASS"
        analyst_note = "Established operating history with no material incidents."
    elif category == "Strong track record with one significant stress event":
        flag = "REVIEW"
        analyst_note = "Generally clean track record with one notable stress event. Review handling of that event and post-event structural changes."
    elif category == "Mixed track record":
        flag = "REVIEW"
        analyst_note = "Mixed historical performance. Review specific incidents and current operational posture."
    elif category == "Material historical incidents, current stability":
        flag = "REVIEW"
        analyst_note = "Material historical operational incidents; current operations stable. Review customer protection track record during prior incidents."
    elif category == "Material historical concerns; current stability":
        flag = "REVIEW"
        analyst_note = "Material historical operational and transparency concerns; current operations stable. Recurring pattern in historical record warrants ongoing monitoring."
    elif category == "Decentralized infrastructure with adversarial regulatory history":
        flag = "FLAG"
        analyst_note = "Decentralized protocol with adversarial regulatory history. Operational continuity is structural (immutable contracts); regulatory posture is the relevant compliance signal."
    else:
        flag = "REVIEW"
        analyst_note = f"Unknown category: '{category}'. Manual review required."
    
    return {
        "dimension": "Operational Track Record",
        "applicable": True,
        "category": category,
        "flag": flag,
        "summary": track_record.get("summary", ""),
        "analyst_note": analyst_note,
        "sources": track_record.get("sources", [])
    }


def assess(entity_id):
    entity_data = load_entity(entity_id)
    
    assessment = {
        "entity_id": entity_id,
        "entity_name": entity_data["entity_name"],
        "entity_type": entity_data["entity_type"],
        "year_founded": entity_data["year_founded"],
        "last_verified": entity_data["last_verified"],
        "dimensions": {
            "dimension_1_licensing": assess_licensing(entity_data),
            "dimension_2_travel_rule": assess_travel_rule(entity_data),
            "dimension_3_sanctions_enforcement": assess_sanctions_enforcement(entity_data),
            "dimension_4_reserve_transparency": assess_reserve_transparency(entity_data),
            "dimension_5a_sanctioned_addresses": assess_sanctioned_addresses(entity_data),
            "dimension_5b_mixer_exposure": assess_mixer_exposure(entity_data),
            "dimension_6_kyc_cdd": assess_kyc_cdd(entity_data),
            "dimension_7_operational_track_record": assess_operational_track_record(entity_data)
        }
    }
    
    return assessment


def count_flags(assessment):
    counts = {"PASS": 0, "REVIEW": 0, "FLAG": 0, "N/A": 0}
    for dim_result in assessment["dimensions"].values():
        flag = dim_result["flag"]
        if flag in counts:
            counts[flag] += 1
    return counts


all_entities = [
    "coinbase", "binance", "kraken", "okx",
    "circle", "paxos", "tether",
    "anchorage", "bitgo", "tornado_cash"
]

for entity_id in all_entities:
    full_assessment = assess(entity_id)
    flag_counts = count_flags(full_assessment)
    
    print(f"=== {full_assessment['entity_name']} ===")
    print(f"Type: {full_assessment['entity_type']}")
    print(f"Last verified: {full_assessment['last_verified']}")
    print(f"Summary: {flag_counts['PASS']} PASS | {flag_counts['REVIEW']} REVIEW | {flag_counts['FLAG']} FLAG | {flag_counts['N/A']} N/A")
    print()
    
    for dim_name, dim_result in full_assessment["dimensions"].items():
        flag = dim_result["flag"]
        dim_label = dim_result["dimension"]
        if dim_result.get("applicable", True):
            category = dim_result.get("category", "N/A")
            note = dim_result.get("analyst_note", "")
            print(f"  [{flag}] {dim_label}")
            print(f"        Category: {category}")
            print(f"        Note: {note}")
        else:
            print(f"  [{flag}] {dim_label}: Not applicable")
        print()
    
    print("-" * 60)
    print()