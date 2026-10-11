
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
REPORT_FILE = BASE_DIR / "reports" / "network_health_summary.csv"
OUTPUT_FILE = BASE_DIR / "reports" / "fault_analysis.csv"


def analyze(row):
    check = row["check"].upper()
    status = row["status"].upper()
    result = row["result"].upper()

    if result == "HEALTHY":
        return "INFO", "No action required"

    if check == "OSPF":
        if status in ("DOWN", "INIT", "ATTEMPT"):
            return "HIGH", "Check router link, IP addressing and OSPF configuration"
        return "MEDIUM", "Inspect OSPF adjacency and neighbor connectivity"

    if check == "INTERFACE":
        if "ADMINISTRATIVELY DOWN" in status:
            return "HIGH", "Check whether the interface should be enabled"
        if "DOWN" in status:
            return "HIGH", "Inspect cable, peer interface and interface configuration"
        return "MEDIUM", "Inspect interface status and protocol"

    return "MEDIUM", "Investigate the reported fault"


def main():
    if not REPORT_FILE.exists():
        print("Run network_analyzer.py first.")
        return

    with open(REPORT_FILE, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    output = []

    for row in rows:
        severity, action = analyze(row)

        item = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "router": row["router"],
            "check": row["check"],
            "item": row["item"],
            "status": row["status"],
            "severity": severity,
            "recommended_action": action
        }
        output.append(item)

        print(
            f"{item['router']} | {item['check']} | "
            f"{item['status']} | {severity}"
        )
        print(f"  Action: {action}")

    fields = [
        "timestamp", "router", "check", "item",
        "status", "severity", "recommended_action"
    ]

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)

    print(f"\nFault analysis saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
