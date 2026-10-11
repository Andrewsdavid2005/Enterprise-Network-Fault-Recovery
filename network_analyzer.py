
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "sample_outputs"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def analyze_interfaces():
    findings = []

    for path in sorted(SOURCE_DIR.glob("*_interfaces.txt")):
        for line in path.read_text(
            encoding="utf-8-sig", errors="replace"
        ).splitlines():
            parts = line.split()

            if len(parts) < 6 or parts[1] != "YES":
                continue

            interface = parts[0]
            ip_address = parts[1] if False else parts[1]
            # IOS output fields: interface, IP, OK?, method,
            # status, protocol. Status may contain spaces.
            ip_address = parts[1] if parts[1] != "YES" else "unknown"

            if len(parts) >= 6:
                status = parts[-2]
                protocol = parts[-1]
                healthy = status == "up" and protocol == "up"

                findings.append({
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "router": path.name.split("_")[0],
                    "check": "INTERFACE",
                    "item": interface,
                    "status": f"{status}/{protocol}",
                    "result": "HEALTHY" if healthy else "CHECK"
                })

    return findings


def analyze_ospf():
    findings = []

    for path in sorted(SOURCE_DIR.glob("*_ospf.txt")):
        for line in path.read_text(
            encoding="utf-8-sig", errors="replace"
        ).splitlines():
            parts = line.split()

            if len(parts) < 6 or not parts[1].isdigit():
                continue

            state = parts[2].upper()
            if not state.startswith(
                ("FULL", "2WAY", "EXSTART", "EXCHANGE",
                 "INIT", "DOWN", "ATTEMPT", "LOADING")
            ):
                continue

            findings.append({
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "router": path.name.split("_")[0],
                "check": "OSPF",
                "item": parts[0],
                "status": state,
                "result": "HEALTHY" if state.startswith("FULL") else "CHECK"
            })

    return findings


def main():
    results = analyze_interfaces() + analyze_ospf()

    report = REPORT_DIR / "network_health_summary.csv"
    fields = ["timestamp", "router", "check", "item", "status", "result"]

    with open(report, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    for row in results:
        print(
            f"{row['router']} | {row['check']} | "
            f"{row['item']} | {row['status']} | {row['result']}"
        )

    print(f"\nCombined report saved: {report}")


if __name__ == "__main__":
    main()
