
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PIPELINE = [
    ("Interface Monitoring", "interface_monitor.py"),
    ("OSPF Monitoring", "ospf_monitor.py"),
    ("Network Analysis", "network_analyzer.py"),
    ("Fault Severity Analysis", "fault_analyzer.py"),
    ("Recovery Planning", "recovery_engine.py"),
]


def main():
    print("=" * 55)
    print(" ENTERPRISE NETWORK AUTOMATION TOOLKIT")
    print("=" * 55)

    for title, script in PIPELINE:
        script_path = BASE_DIR / script

        print(f"\n>>> {title}")

        if not script_path.exists():
            print(f"SKIPPED: {script} not found.")
            print("Create the missing script before running again.")
            return

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=BASE_DIR
        )

        if result.returncode != 0:
            print(f"FAILED: {script}")
            print("Pipeline stopped to prevent misleading reports.")
            return

    print("\n" + "=" * 55)
    print(" AUTOMATION PIPELINE COMPLETED")
    print("=" * 55)
    print("Review your reports folder for the generated CSV files.")


if __name__ == "__main__":
    main()
