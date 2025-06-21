# main.py

import re

# Dictionary of red-flag phrases
RISKY_CLAUSES = {
    "binding arbitration": {
        "explanation": "You waive your right to take the company to court.",
        "weight": 30,
        "category": "⚖️ Legal Rights"
    },
    "we may share your data": {
        "explanation": "Your personal data could be sold or shared with third parties.",
        "weight": 25,
        "category": "🔐 Data Privacy"
    },
    "without notice": {
        "explanation": "Terms can be changed at any time without informing you.",
        "weight": 15,
        "category": "⚠️ General Risks"
    },
    "waive your right": {
        "explanation": "You might be giving up important legal protections.",
        "weight": 15,
        "category": "⚖️ Legal Rights"
    },
    "indemnify": {
        "explanation": "You may be responsible for the company's legal costs.",
        "weight": 10,
        "category": "⚠️ General Risks"
    },
    "third parties": {
        "explanation": "Your information may be provided to outside companies.",
        "weight": 5,
        "category": "🔐 Data Privacy"
    }
}

def scan_tos(text):
    print("\n🔎 Scanning Terms of Service...\n")
    found_clauses = []
    category_hits = {}
    total_score = 0

    # Basic sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for phrase, data in RISKY_CLAUSES.items():
        for sentence in sentences:
            if phrase.lower() in sentence.lower():
                found_clauses.append({
                    "phrase": phrase,
                    "explanation": data["explanation"],
                    "category": data["category"],
                    "sentence": sentence.strip()
                })
                total_score += data["weight"]
                cat = data["category"]
                category_hits[cat] = category_hits.get(cat, 0) + 1
                break  # avoid double-counting

    total_score = min(total_score, 100)

    if total_score >= 70:
        risk_level = "🚨 HIGH RISK"
        risk_meter = "🔥🔥🔥🔥🔥"
    elif total_score >= 40:
        risk_level = "⚠️ MEDIUM RISK"
        risk_meter = "🟡🟡🟡🟡⚪"
    else:
        risk_level = "✅ LOW RISK"
        risk_meter = "✅✅✅✅✅"

    # Results
    if found_clauses:
        print("⚠️ Potential Red Flags Found:\n")
        for item in found_clauses:
            print(f"{item['category']} → \"{item['phrase']}\"")
            print(f"    📝 Sentence: \"{item['sentence']}\"")
            print(f"    💬 Why it's risky: {item['explanation']}\n")
    else:
        print("✅ No major red flags found.")

    # Summary
    print("\n📊 RISK SCORE SUMMARY")
    print("-------------------------")
    print(f"🔢 Total Red Flags: {len(found_clauses)}")
    print(f"🗂 Categories Hit: {len(category_hits)} → {', '.join(category_hits.keys())}")
    print(f"📈 Score: {total_score}/100")
    print(f"🧾 Risk Level: {risk_level}")
    print(f"📉 Risk Meter: {risk_meter}")

    # Category explanations
    print("\n📚 CATEGORY EXPLANATIONS")
    print("-------------------------")
    print("⚖️ Legal Rights → Clauses that waive your right to a fair trial or require arbitration.")
    print("🔐 Data Privacy → Clauses that allow the company to sell, share, or misuse your data.")
    print("⚠️ General Risks → Broad legal language that shifts liability or allows silent changes.")

if __name__ == "__main__":
    print("📄 Terms of Service Analyzer")
    print("-----------------------------")
    print("📋 Paste the **entire Terms of Service** below.")
    print("💡 Press Enter twice when you're done.\n")

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        except EOFError:
            break

    tos_text = "\n".join(lines)
    scan_tos(tos_text)
