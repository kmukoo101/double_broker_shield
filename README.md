# Double Brokering Shield

## Overview

This tool is designed to detect and prevent double brokering in logistics by verifying MC numbers, checking broker activity, flagging suspicious payments, tracking load assignments, and maintaining a watchlist for repeat offenders. It provides a GUI-based input system and generates fraud detection reports to help brokers, carriers, and auditors maintain security in freight transactions.
The goal is to protect brokers, carriers, and shippers from fraudulent transactions. Keep your dataset updated for the best results.

## Features

- **MC Number Verification**: Checks against database (offline) (`fmcsa_data.json`).
- **Communication Validation**: Flags public email domains and VoIP phone numbers.
- **Address Verification**: Compares broker addresses against `address_database.json`.
- **Geo-Verification**: Ensures carrier location aligns with load pickup and delivery.
- **Duplicate Load Detection**: Prevents reposting of the same load.
- **Market Rate Analysis**: Flags suspiciously low bids.
- **Blacklist System**: Tracks fraudulent brokers in `blacklist.json`.
- **Broker Activity Monitoring**: Logs broker email and phone changes in `broker_activity_log.json`.
- **Automated Watchlist System**: Adds brokers to `watchlist.json` after multiple violations.
- **Load Tracking**: Prevents duplicate assignments by storing load IDs in `load_tracking.json`.
- **Document Verification**: Ensures rate confirmations, insurance, and bills of lading are valid.
- **Fraud Report Generation**: Outputs detected fraud into `fraud_detection_report.json`.

## Installation

### For Windows:

1. Open **Command Prompt** and navigate to your root directory:
   ```sh
   cd path\to\project
   ```
2. Create virtual environment:
   ```sh
   python -m venv venv
   ```
3. Activate environment:
   ```sh
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### For macOS/Linux:

1. Open **Terminal** and navigate to your root directory:
   ```sh
   cd /path/to/project
   ```
2. Create virtual environment:
   ```sh
   python3 -m venv venv
   ```
3. Activate environment:
   ```sh
   source venv/bin/activate
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

---

## Run
   ```sh
   python double_brokering_detector.py
   ```
1. Enter load details into GUI.
2. The script will automatically:
   - Check MC legitimacy.
   - Detect duplicate loads.
   - Verify carrier location.
   - Log broker activity.
   - Update fraud report.
3. If fraud is detected, warnings will be displayed, and the broker will be flagged in `watchlist.json`.

### Notes: 
- If any JSON file is missing, the script will create it automatically, but the more data in it, the better.
- The script runs entirely locally and doesn't require third-party API access.
- FMCSA verification currently relies on an offline dataset (`fmcsa_data.json`). If an API integration is needed, modify the `verify_mc_number` function.

#### File Setup:

- **double_brokering_shield.py** → Main script.
- **fmcsa_data.json** → Offline dataset for MC verification.
- **address_database.json** → List of verified broker addresses.
- **carrier_locations.json** → Database of carrier locations for geo-verification.
- **blacklist.json** → Stores fraudulent brokers.
- **broker_activity_log.json** → Logs changes in broker email and phone.
- **watchlist.json** → Tracks high-risk brokers with multiple violations.
- **load_tracking.json** → Prevents duplicate load assignments.
- **fraud_detection_report.json** → Stores detected fraud cases.
