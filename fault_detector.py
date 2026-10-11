
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS_FILE = BASE_DIR / "simulation_results.json"
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"

LOG_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


def classify(status):
    if status == "UP":
        return "HEALTHY"
    if status == "DOWN":
        return "FAULT DETECTED"
    return "UNKNOWN"


def main():
    with open(RESULTS_FILE, encoding="utf-8") as file:
        results = json.load(file)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_file = REPORT_DIR / "fault_report.txt"
    log_file = LOG_DIR / "faults.log"

    lines = [
        "ENTERPRISE NETWORK FAULT REPORT",
        f"Time: {timestamp}",
        "-" * 40
    ]

    alerts = []

    for device, status in results.items():
        status = status.upper()
        diagnosis = classify(status)
        line = f"{device}: {diagnosis}"
        lines.append(line)
        print(line)

        if diagnosis == "FAULT DETECTED":
            alerts.append(f"{timestamp} | {device} | {diagnosis}")

    report_file.write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    if alerts:
        with open(log_file, "a", encoding="utf-8") as file:
            file.write("\n".join(alerts) + "\n")

    print(f"\nReport saved: {report_file}")


if __name__ == "__main__":
    main()
