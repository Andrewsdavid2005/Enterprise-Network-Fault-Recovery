# Enterprise Network Fault Detection & Auto-Recovery

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Networking](https://img.shields.io/badge/Networking-Cisco%20Packet%20Tracer-blue)
![Automation](https://img.shields.io/badge/Automation-Network%20Monitoring-green)
![Status](https://img.shields.io/badge/Project-In%20Development-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Project Overview

**Enterprise Network Fault Detection & Auto-Recovery** is a Python-based network monitoring and troubleshooting project designed to analyze Cisco router interface status, OSPF neighbor information, and network health data.

The project uses a Cisco Packet Tracer enterprise network topology and Python automation scripts to identify potential network faults, classify their severity, generate health reports, and recommend recovery actions.

The current implementation analyzes saved Cisco CLI outputs. It provides a foundation for extending the system into live network monitoring and automated remediation.

## Objectives

- Monitor router interface status and protocol state.
- Analyze OSPF neighbor relationships.
- Identify potential network connectivity and routing issues.
- Classify faults based on severity.
- Generate structured CSV reports for network health.
- Recommend suitable troubleshooting and recovery actions.
- Explore Python-based network automation using Netmiko.
- Improve network reliability through systematic fault analysis.

## Network Topology

The lab consists of three Cisco 2911 routers connected in a triangle topology. Each router connects to a local switch and PC.

```text
                     R1
                 /        \
                /          \
               R2 ---------- R3
               |              |
             Switch          Switch
               |              |
              PC2            PC3

        R1 also connects to its local switch and PC1
```

### Devices and IP addressing

| Device | Interface / Role | IP Address |
|---|---|---|
| R1 | LAN gateway | 192.168.10.1/24 |
| PC1 | End device | 192.168.10.10/24 |
| R2 | LAN gateway | 192.168.20.1/24 |
| PC2 | End device | 192.168.20.10/24 |
| R3 | LAN gateway | 192.168.30.1/24 |
| PC3 | End device | 192.168.30.10/24 |
| R1–R2 | Point-to-point link | 10.0.12.0/30 |
| R1–R3 | Point-to-point link | 10.0.13.0/30 |
| R2–R3 | Point-to-point link | 10.0.23.0/30 |

### Routing configuration

The lab uses **Open Shortest Path First (OSPF)** with the following configuration:

- OSPF process ID: `1`
- OSPF area: `0` (backbone)
- Router IDs: `1.1.1.1`, `2.2.2.2`, and `3.3.3.3`
- LAN interfaces configured as passive where appropriate.

The triangle topology provides multiple paths between routers, making it useful for studying routing behavior and potential link failures.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Automation and analysis |
| Cisco Packet Tracer | Network simulation |
| Cisco IOS CLI | Interface and routing information |
| Netmiko | Python library for network device connections |
| JSON | Device inventory and input data |
| CSV | Health reports and fault analysis |
| PowerShell | Windows terminal and project execution |
| Git and GitHub | Version control and project sharing |

## Project Features

### 1. Interface Monitoring

Reads saved `show ip interface brief` output and analyzes interface status and protocol state.

**Command used in the lab:**

```text
show ip interface brief
```

The analysis can identify conditions such as:

- Interface and protocol both up.
- Interface or protocol down.
- Administratively disabled interfaces.
- Interfaces requiring further investigation.

### 2. OSPF Neighbor Monitoring

Analyzes saved `show ip ospf neighbor` output to check routing adjacency states.

**Command used in the lab:**

```text
show ip ospf neighbor
```

The analysis identifies expected healthy neighbor states and flags other states for investigation.

### 3. Network Health Analysis

Combines interface and OSPF monitoring results into a consolidated health summary.

This helps organize device health information and identify areas requiring troubleshooting.

### 4. Fault Detection and Classification

Analyzes network health information and assigns severity levels to detected issues.

Example classifications:

- **INFO:** No detected fault requiring action.
- **MEDIUM:** A condition needs investigation.
- **HIGH:** A potentially serious routing or connectivity issue requires attention.

The exact severity depends on the conditions recognized by the analysis scripts.

### 5. Recovery Recommendations

Generates suggested actions based on the detected condition.

Examples include:

- Verify interface configuration and physical connectivity.
- Check routing configuration and OSPF neighbor states.
- Investigate management connectivity.
- Review the relevant device logs and CLI output.
- Obtain approval before making configuration changes.

**Current limitation:** The recovery engine generates recommendations; it does not automatically change router configurations or restore failed links.

### 6. SSH Monitoring Experiment

The project includes a Netmiko-based script for attempting SSH connections to network devices.

The connection experiment is separate from the offline analysis pipeline. Cisco Packet Tracer devices may not be reachable directly from the Windows host, depending on the simulation environment and network setup.

Successful SSH access from a simulated PC does not guarantee that the host computer running Python can connect to the same router.

## Project Structure

```text
Enterprise-Network-Fault-Recovery/
│
├── main.py
├── inventory.json
├── requirements.txt
├── interface_monitor.py
├── ospf_monitor.py
├── network_analyzer.py
├── fault_analyzer.py
├── fault_detector.py
├── recovery_engine.py
├── recovery.py
├── ssh_monitor.py
│
├── sample_outputs/
│   ├── R1_interfaces.txt
│   ├── R2_interfaces.txt
│   ├── R3_interfaces.txt
│   ├── R1_ospf.txt
│   ├── R2_ospf.txt
│   └── R3_ospf.txt
│
├── reports/
│   ├── interface_health.csv
│   ├── ospf_health.csv
│   ├── network_health_summary.csv
│   ├── fault_analysis.csv
│   └── recovery_plan.csv
│
└── logs/
    └── faults.log
```

*Note: The listed report and log files are generated outputs and may not exist until the scripts are executed. The exact folder contents depend on your local project version.*

## Installation and Setup

### Prerequisites

Install or prepare:

- Python 3.12
- Visual Studio Code or another Python IDE
- Git
- Cisco Packet Tracer
- A Windows PowerShell terminal

### Step 1: Clone the repository

After publishing the repository to GitHub, run:

```powershell
git clone https://github.com/Andrewsdavid2005/Enterprise-Network-Fault-Recovery.git
cd Enterprise-Network-Fault-Recovery
```

### Step 2: Create a virtual environment

```powershell
py -3.12 -m venv .venv312
```

Activate it:

```powershell
.\.venv312\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the Python executable directly from the environment or adjust your local execution policy as appropriate.

### Step 3: Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` has not yet been populated, add the dependencies actually used by your scripts. For the current Netmiko connection experiment, include:

```text
netmiko>=4.8.0
```

Add other packages only when the project code requires them.

### Step 4: Configure the Packet Tracer lab

1. Build the three-router triangle topology.
2. Connect each router to its LAN switch and PC.
3. Configure the interface IP addresses.
4. Configure OSPF process 1 in area 0.
5. Configure SSH if testing device access.
6. Verify connectivity from the simulated PCs.
7. Save the relevant CLI outputs into `sample_outputs/`.

## Running the Project

### Run the complete offline analysis pipeline

From the project root, activate the virtual environment and run:

```powershell
python main.py
```

The launcher is intended to execute the analysis scripts in sequence:

1. Interface monitoring.
2. OSPF neighbor monitoring.
3. Network health analysis.
4. Fault classification.
5. Recovery plan generation.

The pipeline requires the expected scripts and input files to exist and be compatible with one another.

### Run individual modules

```powershell
python interface_monitor.py
python ospf_monitor.py
python network_analyzer.py
python fault_analyzer.py
python recovery_engine.py
```

For manual fault detection or SSH testing, use:

```powershell
python fault_detector.py
python recovery.py
python ssh_monitor.py
```

Run each command only if the corresponding script is present and its required inputs are configured.

## Generated Reports

| Report | Purpose |
|---|---|
| `interface_health.csv` | Interface and protocol health |
| `ospf_health.csv` | OSPF neighbor state analysis |
| `network_health_summary.csv` | Consolidated network health |
| `fault_analysis.csv` | Fault severity and recommended actions |
| `recovery_plan.csv` | Suggested recovery decisions |
| `fault_report.txt` | Summary of manually supplied fault states |
| `ssh_monitor_report.csv` | Results of SSH connection attempts |
| `faults.log` | Recorded fault events |

Generated filenames may vary depending on the individual scripts and their current configuration.

## Testing and Validation

Use the following tests to validate the project:

1. **Baseline test:** Capture interface and OSPF output when all three routers are operational.
2. **Interface fault test:** Use a controlled lab scenario to create an interface-down condition and capture the new CLI output.
3. **OSPF fault test:** Interrupt a router link and inspect the resulting neighbor states.
4. **Analysis test:** Run the Python modules and confirm that the input changes appear in the generated reports.
5. **Recovery-plan test:** Verify that the reported fault produces an appropriate recommendation.
6. **Connectivity test:** Compare simulated-PC connectivity with the router and OSPF status.

Perform failure tests only in your isolated lab, and restore the original configuration after testing.

## Security Considerations

- Never publish router passwords, API keys, or personal credentials.
- Do not commit `.env` files or local credential files.
- Use environment variables for sensitive settings.
- Sanitize saved CLI outputs before publishing them.
- Do not publish private IP plans, hostnames, or device information if they reveal sensitive details about a real network.
- Test recovery changes in a lab before using them in production.
- Require authorization and appropriate safeguards before implementing automated configuration changes.

## Current Limitations

- The primary monitoring workflow analyzes saved CLI output rather than continuously polling live devices.
- Live Netmiko connections depend on network reachability and device SSH support.
- Packet Tracer simulation devices may not be directly reachable from the host running Python.
- Fault classification depends on the parsing rules and the supplied data.
- Recovery recommendations are generated for review; configuration changes are not automatically applied.
- Results depend on the quality and freshness of the input files.

## Future Enhancements

- Integrate live monitoring with supported network devices.
- Add scheduled polling and fault alerts.
- Improve interface and OSPF parsing for different CLI output formats.
- Implement structured logging and historical health tracking.
- Add a dashboard for network status visualization.
- Introduce configurable recovery workflows with approval and rollback.
- Add unit tests for parsing, fault classification, and recovery decisions.
- Expand support for additional routing protocols and device types.

## Learning Outcomes

Through this project, I practiced:

- Cisco router configuration and troubleshooting.
- OSPF neighbor formation and routing behavior.
- Python scripting for network operations.
- Parsing CLI output and generating CSV reports.
- Fault classification and recovery planning.
- Using Netmiko to explore SSH-based network automation.
- Organizing a multi-script Python project with Git and GitHub.

## Author

**Andrews GnanaSelvin D**

- GitHub: [Andrewsdavid2005](https://github.com/Andrewsdavid2005)
- LinkedIn: [Andrews GnanaSelvin D](https://www.linkedin.com/in/andrews-gnana-selvin-d)

## License

This project is licensed under the MIT License. Add a `LICENSE` file containing the MIT License text before describing the repository as officially licensed under MIT.

---

If you find this project useful for learning network troubleshooting and Python automation, feel free to explore the code and suggest improvements.
