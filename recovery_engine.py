
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "reports" / "fault_analysis.csv"
OUTPUT_FILE = BASE_DIR / "reports" / "recovery_plan.csv"


def decide(row):
    severity = row["severity"].upper()
    check = row["check"].upper()
    status = row["status"].upper()

    if severity == "INFO":
        return "NO_ACTION", "No fault detected"

    if check == "INTERFACE":
        if "ADMINISTRATIVELY DOWN" in status:
            return (
                "MANUAL_APPROVAL",
                "Confirm maintenance status before enabling interface"
            )
        return (
            "INVESTIGATE",
            "Check physical link, peer interface, and configuration"
        )

    if check == "OSPF":
        return (
            "INVESTIGATE",
            "Verify neighbor state, IP connectivity, and OSPF configuration"
        )

    return "INVESTIGATE", "Review device output before recovery"


def main():
    if not INPUT_FILE.exists():
        print("Run network_analyzer.py and fault_analyzer.py first.")
        return

    with open(INPUT_FILE, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    plan = []

    for row in rows:
        decision, action = decide(row)

        item = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "router": row["router"],
            "check": row["check"],
            "item": row["item"],
            "severity": row["severity"],
            "decision": decision,
            "recommended_action": action
        }
        plan.append(item)

        print(
            f"{item['router']} | {item['severity']} | "
            f"{decision}: {action}"
        )

    fields = [
        "timestamp", "router", "check", "item",
        "severity", "decision", "recommended_action"
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(plan)

    print(f"\nRecovery plan saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
