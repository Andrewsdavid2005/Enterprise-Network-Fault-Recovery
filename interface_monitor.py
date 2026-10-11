
import re
import csv
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "sample_outputs"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)


def check_interfaces(file_path):
    findings = []

    text = file_path.read_text(encoding="utf-8", errors="replace")

    for line in text.splitlines():
        # Match interface rows from "show ip interface brief"
        match = re.match(
            r"^\s*(\S+)\s+(\S+)\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s*$",
            line
        )

        if not match:
            continue

        interface, ip, status, protocol = match.groups()

        if interface.lower() == "interface":
            continue

        healthy = status == "up" and protocol == "up"

        findings.append({
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "router": file_path.name.split("_")[0],
            "interface": interface,
            "ip_address": ip,
            "status": status,
            "protocol": protocol,
            "result": "HEALTHY" if healthy else "FAULT DETECTED"
        })

    return findings


def main():
    files = sorted(SOURCE_DIR.glob("*_interfaces.txt"))

    if not files:
        print(f"No interface files found in {SOURCE_DIR}")
        return

    all_findings = []

    for file_path in files:
        print(f"\nChecking {file_path.name}")
        findings = check_interfaces(file_path)

        for item in findings:
            print(
                f"{item['router']} | {item['interface']} | "
                f"{item['status']}/{item['protocol']} | "
                f"{item['result']}"
            )
            all_findings.append(item)

    report_file = REPORT_DIR / "interface_health.csv"

    with open(report_file, "w", newline="", encoding="utf-8") as file:
        fields = [
            "timestamp", "router", "interface", "ip_address",
            "status", "protocol", "result"
        ]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_findings)

    print(f"\nReport saved: {report_file}")


if __name__ == "__main__":
    main()
