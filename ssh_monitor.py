
from netmiko import ConnectHandler
from datetime import datetime
from pathlib import Path
import csv

ROUTERS = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.10.1",
        "username": "netadmin",
        "password": "NetAuto@123",
        "name": "R1",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.20.1",
        "username": "netadmin",
        "password": "NetAuto@123",
        "name": "R2",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.30.1",
        "username": "netadmin",
        "password": "NetAuto@123",
        "name": "R3",
    },
]

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def monitor_router(router):
    print(f"\nConnecting to {router['name']} ({router['host']})")

    try:
        with ConnectHandler(**{
            key: value
            for key, value in router.items()
            if key != "name"
        }) as connection:

            interfaces = connection.send_command(
                "show ip interface brief"
            )
            ospf = connection.send_command(
                "show ip ospf neighbor"
            )

            print("\n--- Interface Status ---")
            print(interfaces)
            print("\n--- OSPF Neighbors ---")
            print(ospf)

            return {
                "timestamp": datetime.now().isoformat(
                    timespec="seconds"
                ),
                "router": router["name"],
                "ip": router["host"],
                "ssh_status": "SUCCESS",
                "interface_output": interfaces.replace(
                    "\n", " | "
                ),
                "ospf_output": ospf.replace("\n", " | "),
                "error": "",
            }

    except Exception as error:
        print(f"Connection failed: {error}")
        return {
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "router": router["name"],
            "ip": router["host"],
            "ssh_status": "FAILED",
            "interface_output": "",
            "ospf_output": "",
            "error": str(error),
        }


def main():
    results = [monitor_router(router) for router in ROUTERS]

    report_file = REPORT_DIR / "ssh_monitor_report.csv"

    with open(
        report_file, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nMonitoring finished. Report: {report_file}")


if __name__ == "__main__":
    main()
