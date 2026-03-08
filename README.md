# Braava M6 Behavioral Evaluation

A systematic QA evaluation framework for the iRobot Braava Jet M6 (6110) robot mop. Applies structured testing methodology to a physical robot — defining expected behavior, logging real data via the robot's local API, and analyzing results across repeated runs.

## Why This Project

Physical AI systems require the same rigorous behavioral evaluation as software. This project treats the M6 as a system under test — not just a consumer device — and builds tooling to evaluate it systematically.

## Test Categories (Planned)

- **Dock Return Reliability** — does the robot successfully return to dock after every mission?
- **Coverage Consistency** — does it report similar square footage across identical runs?
- **Mission Duration Variance** — how consistent is cleaning time for the same room?
- **Battery Drain Rate** — is power consumption consistent across missions?
- **Error Rate Analysis** — frequency and categorization of error codes over time
- **Surface Behavior** — manual evaluation across hardwood, tile, and transitions

## How It Works

The M6 exposes its state locally over MQTT via an unofficial API reverse engineered by the community. This project uses `roombapy` to connect directly over WiFi, poll robot state in real time during cleaning missions, and log structured JSON data for analysis.

## Project Structure
```
braava-m6-eval/
├── connect.py          # connection test — verify credentials work
├── collect_state.py    # logs robot state during a live cleaning run
├── analyze_results.py  # parses logs and generates summary report
├── push.sh             # git workflow automation
├── data/runs/          # timestamped JSON logs per test run (gitignored)
├── results/            # aggregated CSV results (gitignored)
└── requirements.txt    
```

## Setup
```bash
git clone https://github.com/MichaelNguyenz229/braava-m6-eval.git
cd braava-m6-eval

python3 -m venv venv            # If on Mac/Linux
source venv/bin/activate      

# python -m venv venv           # If on Windows
# source venv/Scripts/activate  

pip install -r requirements.txt
```

Create a `.env` file with your robot credentials:
```
ROBOT_IP=192.168.X.X
BLID=your_blid
PASSWORD=your_password
```

Then run the connection test:
```bash
python connect.py
```

## Status

 In progress — active data collection pending

## Author

Michael Nguyen