
from pathlib import Path
from datetime import datetime
import csv

BASE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = BASE_DIR / "sample_outputs"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def check_ospf(file_path):
    results = []

    text = file_path.read_text(
        encoding="utf-8-sig",
        errors="replace"
    )

    for line in text.splitlines():
        parts = line.split()

        # Expected: ID, Priority, State, Dead Time, Address, Interface
        if len(parts) < 6:
            continue

        # Skip headers and non-neighbor lines
        if not parts[1].isdigit():
            continue

        state = parts[2].upper()

        valid_states = (
            "FULL", "2WAY", "EXSTART", "EXCHANGE",
            "INIT", "DOWN", "ATTEMPT", "LOADING"
        )

        if not state.startswith(valid_states):
            continue

        results.append({
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "router": file_path.name.split("_")[0],
            "neighbor_id": parts[0],
            "state": state,
            "address": parts[4],
            "interface": parts[5],
            "result": "HEALTHY" if state.startswith("FULL") else "CHECK"
        })

    return results


def main():
    files = sorted(SOURCE_DIR.glob("*_ospf.txt"))

    if not files:
        print(f"No OSPF files found in {SOURCE_DIR}")
        return

    all_results = []

    for file_path in files:
        print(f"\nChecking {file_path.name}")
        results = check_ospf(file_path)

        if not results:
            print("No neighbors parsed. Check file contents.")
            print("First lines of the file:")
            print("\n".join(
                file_path.read_text(
                    encoding="utf-8-sig", errors="replace"
                ).splitlines()[:5]
            ))

        for item in results:
            print(
                f"{item['router']} -> {item['neighbor_id']} | "
                f"{item['state']} | {item['result']}"
            )
            all_results.append(item)

    report = REPORT_DIR / "ospf_health.csv"
    fields = [
        "timestamp", "router", "neighbor_id",
        "state", "address", "interface", "result"
    ]

    with open(report, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nOSPF report saved: {report}")


if __name__ == "__main__":
    main()
