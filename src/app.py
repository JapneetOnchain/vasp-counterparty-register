import streamlit as st
from assess import assess, count_flags
from datetime import date

# Page config
st.set_page_config(
    page_title="VASP Counterparty Risk Register",
    page_icon="🛡️",
    layout="wide"
)

# Entity options
entity_options = {
    "Coinbase": "coinbase",
    "Binance": "binance",
    "Kraken": "kraken",
    "OKX": "okx",
    "Circle": "circle",
    "Paxos": "paxos",
    "Tether": "tether",
    "Anchorage Digital": "anchorage",
    "BitGo": "bitgo",
    "Tornado Cash protocol": "tornado_cash"
}

# Dimension names for weight config (display name -> dimension key)
dimension_weights_config = {
    "Licensing": "dimension_1_licensing",
    "Travel Rule": "dimension_2_travel_rule",
    "Sanctions/Enforcement": "dimension_3_sanctions_enforcement",
    "Reserve Transparency": "dimension_4_reserve_transparency",
    "Sanctioned Address Exposure": "dimension_5a_sanctioned_addresses",
    "Mixer Exposure": "dimension_5b_mixer_exposure",
    "KYC/CDD Posture": "dimension_6_kyc_cdd",
    "Operational Track Record": "dimension_7_operational_track_record"
}

# Initialize weights in session state if not set
if "weights" not in st.session_state:
    st.session_state.weights = {
        display_name: 5 for display_name in dimension_weights_config.keys()
    }

# Helper functions
def flag_emoji(flag):
    if flag == "PASS":
        return "🟢"
    elif flag == "REVIEW":
        return "🟡"
    elif flag == "FLAG":
        return "🔴"
    else:
        return "⚪"

def flag_score(flag):
    if flag == "PASS":
        return 10
    elif flag == "REVIEW":
        return 5
    elif flag == "FLAG":
        return 0
    else:
        return None

def calculate_weighted_score(assessment, weights):
    total_weight = 0
    weighted_sum = 0
    for display_name, dim_key in dimension_weights_config.items():
        if dim_key not in assessment["dimensions"]:
            continue
        dim_result = assessment["dimensions"][dim_key]
        score = flag_score(dim_result["flag"])
        if score is None:
            continue
        weight = weights.get(display_name, 5)
        if weight == 0:
            continue
        total_weight += weight
        weighted_sum += score * weight
    if total_weight == 0:
        return None
    return weighted_sum / total_weight

def check_hard_blockers(assessment):
    blockers = []
    dims = assessment["dimensions"]
    if "dimension_2_travel_rule" in dims:
        if dims["dimension_2_travel_rule"].get("category") == "N/A — decentralized smart contract, no VASP":
            blockers.append("Cannot satisfy Travel Rule (decentralized protocol)")
    if "dimension_6_kyc_cdd" in dims:
        if dims["dimension_6_kyc_cdd"].get("category") == "No KYC by design":
            blockers.append("No KYC layer by design (decentralized protocol)")
    if "dimension_1_licensing" in dims:
        if dims["dimension_1_licensing"].get("category") == "No identifiable major-jurisdiction authorization (by design)":
            blockers.append("No regulatory authorization (decentralized infrastructure)")
    return blockers

def get_recommendation(assessment, weights, flag_tolerance):
    blockers = check_hard_blockers(assessment)
    if blockers:
        return {
            "decision": "DECLINE",
            "rationale": "Structural barriers to onboarding as regulated counterparty.",
            "blockers": blockers,
            "score": None
        }
    
    score = calculate_weighted_score(assessment, weights)
    flag_count = count_flags(assessment)["FLAG"]
    
    if flag_count > flag_tolerance:
        return {
            "decision": "DECLINE",
            "rationale": f"FLAG count ({flag_count}) exceeds risk tolerance threshold ({flag_tolerance}).",
            "blockers": [],
            "score": score
        }
    
    if score is None:
        return {
            "decision": "MANUAL REVIEW",
            "rationale": "Insufficient applicable dimensions for automated scoring.",
            "blockers": [],
            "score": None
        }
    
    if score >= 8.0:
        decision = "APPROVE"
        rationale = "Strong scoring across weighted dimensions; no material concerns."
    elif score >= 6.0:
        decision = "APPROVE WITH CONDITIONS"
        rationale = "Acceptable risk profile with specific concerns that warrant documented conditions."
    else:
        decision = "DECLINE"
        rationale = "Weighted scoring below threshold; risk profile not acceptable for standard onboarding."
    
    return {
        "decision": decision,
        "rationale": rationale,
        "blockers": [],
        "score": score
    }

def generate_memo(assessment, recommendation, weights, flag_tolerance):
    today = date.today().isoformat()
    flag_counts = count_flags(assessment)
    
    memo = f"""# Counterparty Decision Memo

## {assessment['entity_name']}

**Date:** {today}  
**Entity Type:** {assessment['entity_type']}  
**Last Verified:** {assessment['last_verified']}  
**Recommendation:** **{recommendation['decision']}**

---

## Risk Configuration Applied

| Dimension | Weight |
|-----------|--------|
"""
    for display_name, weight in weights.items():
        memo += f"| {display_name} | {weight}/10 |\n"
    
    memo += f"\n**FLAG Tolerance:** {flag_tolerance}\n\n---\n\n"
    
    if recommendation['score'] is not None:
        memo += f"## Weighted Score: {recommendation['score']:.1f} / 10.0\n\n"
    
    memo += f"## Rationale\n\n{recommendation['rationale']}\n\n"
    
    if recommendation['blockers']:
        memo += "### Hard Blockers\n\n"
        for blocker in recommendation['blockers']:
            memo += f"- {blocker}\n"
        memo += "\n"
    
    memo += f"""## Summary of Findings

- {flag_counts['PASS']} dimensions PASS
- {flag_counts['REVIEW']} dimensions REVIEW
- {flag_counts['FLAG']} dimensions FLAG
- {flag_counts['N/A']} dimensions N/A

---

## Dimension Detail

"""
    
    for dim_key, dim_result in assessment["dimensions"].items():
        flag = dim_result["flag"]
        dim_label = dim_result["dimension"]
        memo += f"### {flag_emoji(flag)} {dim_label} — {flag}\n\n"
        if dim_result.get("applicable", True):
            memo += f"**Category:** {dim_result.get('category', 'N/A')}\n\n"
            memo += f"**Note:** {dim_result.get('analyst_note', '')}\n\n"
            sources = dim_result.get("sources", [])
            if sources:
                memo += "**Sources:**\n"
                for src in sources:
                    memo += f"- {src}\n"
                memo += "\n"
        else:
            memo += "Not applicable for this entity type.\n\n"
    
    memo += """---

## Methodology

This recommendation was generated using the VASP Counterparty Risk Register framework — a 7-dimension structured assessment combining static regulatory data with on-chain measurement.

**Decision logic:**
1. Hard blockers (structural impossibilities) trigger automatic DECLINE
2. FLAG count exceeding user-defined tolerance triggers DECLINE
3. Weighted score 8.0+ triggers APPROVE
4. Weighted score 6.0-8.0 triggers APPROVE WITH CONDITIONS
5. Weighted score below 6.0 triggers DECLINE

**Limitations:**
- Public information only; non-public regulatory examination findings not incorporated
- 1-hop on-chain measurement; multi-hop intermediated flows require licensed analytics
- Categorical assessments updated periodically; refer to last_verified date

Full framework: github.com/JapneetOnchain
Live on-chain dashboard: https://dune.com/japneet/vasp-counterparty-register

---

*Generated by VASP Counterparty Risk Register v0.1*
"""
    
    return memo

# Sidebar
with st.sidebar:
    st.title("🛡️ VASP Risk Register")
    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "A counterparty risk assessment toolkit for crypto VASPs. "
        "Combines structured regulatory data with on-chain measurement."
    )
    st.markdown("---")
    st.markdown("### Resources")
    st.markdown("- [📊 Live Dune Dashboard](https://dune.com/japneet/vasp-counterparty-register)")
    st.markdown("- [💻 GitHub Repository](https://github.com/JapneetOnchain)")
    st.markdown("---")
    st.markdown("### Author")
    st.markdown(
        "**Japneet Singh**  \n"
        "Crypto compliance & on-chain forensics  \n"
        "[github.com/JapneetOnchain](https://github.com/JapneetOnchain)"
    )

# Main page header
st.title("VASP Counterparty Risk Register")
st.markdown(
    "**A reproducible 7-dimension counterparty assessment toolkit for crypto VASPs.**  \n"
    "Combines structured regulatory data with on-chain measurement. "
    "Configure your firm's risk priorities, generate decision recommendations, "
    "export defensible compliance memos."
)
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 Single Entity Assessment", "⚖️ Comparison View", "🎯 Risk Configuration"])

# === TAB 1: Single Entity ===
with tab1:
    st.subheader("Assess a single entity")
    
    col_select, col_tolerance = st.columns([2, 1])
    with col_select:
        selected_name = st.selectbox(
            "Select an entity:",
            options=list(entity_options.keys()),
            key="tab1_entity_select"
        )
    with col_tolerance:
        flag_tolerance = st.slider(
            "FLAG tolerance:",
            min_value=0,
            max_value=7,
            value=2,
            help="Maximum number of FLAGs your firm tolerates before recommending DECLINE"
        )
    
    selected_id = entity_options[selected_name]
    
    if st.button("Run Assessment", type="primary", key="tab1_run"):
        full_assessment = assess(selected_id)
        flag_counts = count_flags(full_assessment)
        recommendation = get_recommendation(full_assessment, st.session_state.weights, flag_tolerance)
        
        st.markdown(f"## {full_assessment['entity_name']}")
        
        col_meta1, col_meta2, col_meta3 = st.columns(3)
        with col_meta1:
            st.metric("Type", full_assessment['entity_type'].replace("_", " ").title())
        with col_meta2:
            st.metric("Last Verified", full_assessment['last_verified'])
        with col_meta3:
            if recommendation['score'] is not None:
                st.metric("Weighted Score", f"{recommendation['score']:.1f} / 10")
            else:
                st.metric("Weighted Score", "N/A")
        
        decision = recommendation['decision']
        if decision == "APPROVE":
            st.success(f"### ✅ Recommendation: {decision}\n{recommendation['rationale']}")
        elif decision == "APPROVE WITH CONDITIONS":
            st.warning(f"### ⚠️ Recommendation: {decision}\n{recommendation['rationale']}")
        elif decision == "MANUAL REVIEW":
            st.info(f"### 🔍 Recommendation: {decision}\n{recommendation['rationale']}")
        else:
            st.error(f"### 🛑 Recommendation: {decision}\n{recommendation['rationale']}")
        
        if recommendation['blockers']:
            st.markdown("**Hard Blockers:**")
            for b in recommendation['blockers']:
                st.markdown(f"- {b}")
        
        st.markdown("### Summary")
        col_p, col_r, col_f, col_n = st.columns(4)
        with col_p:
            st.metric("🟢 PASS", flag_counts['PASS'])
        with col_r:
            st.metric("🟡 REVIEW", flag_counts['REVIEW'])
        with col_f:
            st.metric("🔴 FLAG", flag_counts['FLAG'])
        with col_n:
            st.metric("⚪ N/A", flag_counts['N/A'])
        
        st.markdown("---")
        
        st.markdown("### Dimension Detail")
        for dim_key, dim_result in full_assessment["dimensions"].items():
            flag = dim_result["flag"]
            dim_label = dim_result["dimension"]
            
            with st.expander(f"{flag_emoji(flag)} {dim_label} — **{flag}**", expanded=(flag != "N/A" and flag != "PASS")):
                if dim_result.get("applicable", True):
                    st.markdown(f"**Category:** {dim_result.get('category', 'N/A')}")
                    st.markdown(f"**Summary:** {dim_result.get('summary', '')}")
                    st.markdown(f"**Analyst Note:** {dim_result.get('analyst_note', '')}")
                    sources = dim_result.get("sources", [])
                    if sources:
                        st.markdown("**Sources:**")
                        for src in sources:
                            st.markdown(f"- {src}")
                else:
                    st.markdown("Not applicable for this entity type.")
        
        st.markdown("---")
        
        st.markdown("### 📄 Decision Memo")
        st.markdown("Generate a defensible decision memo for risk committee review.")
        memo = generate_memo(full_assessment, recommendation, st.session_state.weights, flag_tolerance)
        st.download_button(
            label="⬇️ Download Decision Memo (Markdown)",
            data=memo,
            file_name=f"decision_memo_{selected_id}_{date.today().isoformat()}.md",
            mime="text/markdown"
        )
        with st.expander("Preview memo"):
            st.markdown(memo)

# === TAB 2: Comparison ===
with tab2:
    st.subheader("Compare entities side-by-side")
    st.markdown("Select 2-3 entities to compare across all dimensions.")
    
    selected_for_comparison = st.multiselect(
        "Select entities (max 3):",
        options=list(entity_options.keys()),
        default=["Coinbase", "Tether"],
        max_selections=3
    )
    
    if len(selected_for_comparison) >= 2:
        if st.button("Compare", type="primary", key="tab2_compare"):
            assessments = {
                name: assess(entity_options[name]) 
                for name in selected_for_comparison
            }
            
            cols = st.columns(len(selected_for_comparison) + 1)
            cols[0].markdown("**Dimension**")
            for i, name in enumerate(selected_for_comparison):
                cols[i + 1].markdown(f"**{name}**")
            
            st.markdown("---")
            
            cols = st.columns(len(selected_for_comparison) + 1)
            cols[0].markdown("**Weighted Score**")
            for i, name in enumerate(selected_for_comparison):
                score = calculate_weighted_score(assessments[name], st.session_state.weights)
                if score is not None:
                    cols[i + 1].markdown(f"**{score:.1f} / 10**")
                else:
                    cols[i + 1].markdown("N/A")
            
            cols = st.columns(len(selected_for_comparison) + 1)
            cols[0].markdown("**Recommendation**")
            for i, name in enumerate(selected_for_comparison):
                rec = get_recommendation(assessments[name], st.session_state.weights, 2)
                cols[i + 1].markdown(f"**{rec['decision']}**")
            
            st.markdown("---")
            
            for display_name, dim_key in dimension_weights_config.items():
                cols = st.columns(len(selected_for_comparison) + 1)
                cols[0].markdown(f"**{display_name}**")
                for i, name in enumerate(selected_for_comparison):
                    dim_result = assessments[name]["dimensions"].get(dim_key, {})
                    flag = dim_result.get("flag", "?")
                    category = dim_result.get("category", "N/A")
                    cols[i + 1].markdown(f"{flag_emoji(flag)} **{flag}**  \n_{category}_")
                st.markdown("")
    else:
        st.info("Select at least 2 entities to compare.")

# === TAB 3: Risk Configuration ===
with tab3:
    st.subheader("Configure your firm's risk priorities")
    st.markdown(
        "Set the weight (0-10) for each dimension based on your firm's specific risk priorities. "
        "Weights affect the weighted scoring used for decision recommendations across all entities. "
        "These settings persist across tabs in this session."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        for display_name in list(dimension_weights_config.keys())[:4]:
            st.session_state.weights[display_name] = st.slider(
                display_name,
                min_value=0,
                max_value=10,
                value=st.session_state.weights[display_name],
                key=f"weight_{display_name}"
            )
    
    with col2:
        for display_name in list(dimension_weights_config.keys())[4:]:
            st.session_state.weights[display_name] = st.slider(
                display_name,
                min_value=0,
                max_value=10,
                value=st.session_state.weights[display_name],
                key=f"weight_{display_name}"
            )
    
    st.markdown("---")
    
    if st.button("Apply weights and rank all entities", type="primary"):
        st.markdown("### Ranked Output (highest to lowest weighted score)")
        
        all_results = []
        for name, eid in entity_options.items():
            assessment = assess(eid)
            score = calculate_weighted_score(assessment, st.session_state.weights)
            recommendation = get_recommendation(assessment, st.session_state.weights, 2)
            all_results.append({
                "name": name,
                "score": score if score is not None else -1,
                "decision": recommendation["decision"],
                "flag_counts": count_flags(assessment)
            })
        
        all_results.sort(key=lambda x: x["score"], reverse=True)
        
        for i, result in enumerate(all_results, start=1):
            score_display = f"{result['score']:.1f}" if result['score'] >= 0 else "N/A"
            decision = result["decision"]
            
            if decision == "APPROVE":
                indicator = "🟢"
            elif decision == "APPROVE WITH CONDITIONS":
                indicator = "🟡"
            elif decision == "MANUAL REVIEW":
                indicator = "🔵"
            else:
                indicator = "🔴"
            
            fc = result["flag_counts"]
            st.markdown(
                f"**{i}. {indicator} {result['name']}** — Score: {score_display} | "
                f"{decision} | "
                f"🟢 {fc['PASS']} 🟡 {fc['REVIEW']} 🔴 {fc['FLAG']} ⚪ {fc['N/A']}"
            )