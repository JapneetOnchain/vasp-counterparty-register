import json

def load_entity(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data

def assess_licensing(category):
    if category == "Comprehensive multi-jurisdiction":
        flag = "PASS"
        note = "Strong regulatory standing across major jurisdictions."
    elif category == "Significant single-jurisdiction":
        flag = "REVIEW"
        note = "Adequate licensing but concentrated in one jurisdiction."
    elif category == "Limited or partial":
        flag = "FLAG"
        note = "Material gaps in major-jurisdiction authorization. Manual review required."
    else:
        flag = "FLAG"
        note = "No identifiable major-jurisdiction authorization. High counterparty risk."
    
    return {"flag": flag, "note": note}

def assess_entity(entity_data):
    name = entity_data["name"]
    licensing_result = assess_licensing(entity_data["licensing_category"])
    
    assessment = {
        "entity": name,
        "year_founded": entity_data["year_founded"],
        "licensing_flag": licensing_result["flag"],
        "licensing_note": licensing_result["note"]
    }
    return assessment

entity_files = ["coinbase.json", "binance.json", "tether.json"]

for filename in entity_files:
    entity_data = load_entity(filename)
    assessment = assess_entity(entity_data)
    
    print(f"=== {assessment['entity']} ===")
    print(f"Founded: {assessment['year_founded']}")
    print(f"Licensing flag: {assessment['licensing_flag']}")
    print(f"Note: {assessment['licensing_note']}")
    print()