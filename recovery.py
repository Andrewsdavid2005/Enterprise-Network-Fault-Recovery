
def recommend_recovery(device, status):
    if status == "UP":
        return f"{device}: No action required."

    if status == "DOWN":
        return (
            f"{device}: Investigate reachability, "
            "interfaces, and routing before recovery."
        )

    return f"{device}: Status unknown. Run diagnostics first."


if __name__ == "__main__":
    devices = {
        "R1": "UP",
        "R2": "DOWN",
        "R3": "UP"
    }

    print("\nNETWORK RECOVERY RECOMMENDATIONS")
    print("-" * 40)

    for device, status in devices.items():
        print(recommend_recovery(device, status))
