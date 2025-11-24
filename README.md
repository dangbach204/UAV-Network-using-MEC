# UAV-Mounted MEC Handover Simulation with Migration Penalty

## Overview

This project implements an advanced **UAV-mounted Mobile Edge Computing (MEC)** simulation using **NS-3 (version 3.43)**. The simulation models three aerial UAV base stations serving mobile User Equipment (UE) in an urban environment, with a focus on handover management, service migration penalties, and quality of service metrics.

## Key Features

### Network Architecture

- **3 UAV Base Stations**: Flying in patrol patterns at 30m altitude
- **3 User Equipment (UE)**:
  - UE 1 & 3: Static users with random walk mobility
  - UE 2: Mobile user traversing between coverage areas
- **LTE Network**: Full EPC architecture with PGW, SGW, and MME
- **Remote Server**: Centralized application server

### Advanced Capabilities

- **Realistic Handover Simulation**: A3-RSRP algorithm with configurable hysteresis
- **MEC Service Migration**: Container migration penalty modeling (50ms delay)
- **Quality Metrics**: RSRP, SINR, throughput, jitter, packet loss
- **Flow Monitoring**: End-to-end network statistics via FlowMonitor
- **Visual Animation**: NetAnim XML output for network visualization
- **Comprehensive Logging**: 10+ CSV files for detailed analysis

## Technical Configuration

### Propagation Model

```cpp
Pathloss Model: LogDistancePropagationLossModel
Exponent: 3.0 (urban environment)
Reference Loss: 46.67 dB (2GHz LTE standard)
```

### Handover Parameters

```cpp
Algorithm: A3RsrpHandoverAlgorithm
Hysteresis: 0.1 dB (low sensitivity for frequent handovers)
Time to Trigger: 20 ms
```

### Traffic Configuration

```cpp
Application: UDP downlink traffic
Data Rate: ~2 Mbps per UE
Packet Size: 1472 bytes
Interval: 4 ms between packets
```

### MEC Offloading Logic

- **Task Size**: 0.1 Mbits data + 2000 Megacycles computation
- **Decision**: Offload if (transmission + processing + migration) < local execution
- **Migration Penalty**: 50ms added when UE changes serving cell
- **UAV CPU Speed**: 5000 cycles/s
- **Local CPU Speed**: 1000 cycles/s

## Project Structure

```
project/
├── mode1.cc                              # Main simulation source code
├── combined_charts.py                    # Visualization script (2x4 grid)
├── README.md                             # This file
└── output/
    ├── scenario1_final_throughput.csv    # Per-UE throughput over time
    ├── scenario1_final_rsrp.csv          # Signal strength measurements
    ├── scenario1_final_sinr.csv          # Signal quality metrics
    ├── scenario1_final_handover_quality.csv  # Handover event details
    ├── scenario1_final_mec_offload.csv   # MEC task offloading logs
    ├── scenario1_final_flow_stats.csv    # End-to-end flow statistics
    ├── scenario1_final_ue_position.csv   # UE mobility traces
    ├── scenario1_final_uav_position.csv  # UAV patrol paths
    ├── scenario1_final_cellid.csv        # Cell attachment history
    ├── handover_trace.csv                # Simplified HO events
    └── scenario1_final.xml               # NetAnim visualization file
```

## Installation & Requirements

### Prerequisites

- **NS-3 version 3.43** (or compatible)
- **C++17 compiler** (g++ 7.0+)
- **Python 3.8+** with libraries:
  - pandas
  - matplotlib
  - seaborn
  - numpy

### NS-3 Modules Required

- core-module
- network-module
- internet-module
- mobility-module
- lte-module
- applications-module
- point-to-point-module
- flow-monitor-module
- buildings-module
- netanim-module

## Build & Run

### Step 1: Compile the Simulation

```bash
# Copy mode1.cc to NS-3 scratch directory
cp mode1.cc ~/ns-allinone-3.43/ns-3.43/scratch/

# Navigate to NS-3 root
cd ~/ns-allinone-3.43/ns-3.43/

# Build the project
./ns3 build

# Run simulation (100 seconds)
./ns3 run "scratch/mode1 --simTime=99"
```

### Step 2: Generate Visualizations

```bash
# Ensure CSV files are in the same directory
python3 combined_charts.py
```

**Output**: `Full_UAV_MEC_Report_2x4.png` (8-panel comprehensive report)

## Visualization Charts

The Python script generates an 8-panel visualization:

### Top Row (Performance Comparison)

- **(A)** UE 1 Throughput (Static User)
- **(B)** UE 3 Throughput (Static User)
- **(C)** 3-UE Throughput Comparison (Mobile vs Static)
- **(D)** Jitter Comparison (Bar Chart)

### Bottom Row (Detailed Analysis)

- **(E)** RSRP with Handover Events (Signal Strength)
- **(F)** Throughput Stability during Handovers
- **(G)** MEC Service Latency with Migration Penalty
- **(H)** SINR Variation with Nakagami Fading

## Key Results & Metrics

### Expected Observations

1. **Handover Frequency**: UE 2 triggers ~2-3 handovers during 100s simulation
2. **Migration Impact**: 50ms latency spike when UE changes serving UAV
3. **Throughput Degradation**: ~10-30% during handover transition
4. **Static UE Performance**: UE 1 & 3 maintain stable ~3 Mbps throughput
5. **RSRP Threshold**: Handovers occur when target cell RSRP exceeds serving cell by 0.1 dB

### Performance Indicators

## Customization Guide

### Modify UAV Flight Patterns

Edit waypoints in `mode1.cc` (lines 300-330):

```cpp
uav1->AddWaypoint(Waypoint(Seconds(25), Vector(120, 80, 30)));
```

### Adjust Handover Sensitivity

Change hysteresis parameter (line 240):

```cpp
lteHelper->SetHandoverAlgorithmAttribute("Hysteresis", DoubleValue(0.5));
```

### Tune Migration Penalty

Modify delay in `GenerateMecTask()` function (line 65):

```cpp
migrationPenalty = 0.100;
```

### Change Traffic Load

Adjust UDP client interval (line 430):

```cpp
client.SetAttribute("Interval", TimeValue(MilliSeconds(2.0)));
```

## Troubleshooting

### Common Issues

**Problem**: Simulation crashes with segmentation fault

```bash
# Solution: Check NS-3 version compatibility
./ns3 --version  # Should be 3.43
```

**Problem**: Empty CSV files generated

```bash
# Solution: Ensure output directory has write permissions
chmod 755 .
```

**Problem**: Python script shows "File not found"

```bash
# Solution: Run from the directory containing CSV files
cd ~/ns-allinone-3.43/ns-3.43/
python3 combined_charts.py
```

**Problem**: NetAnim file too large (>1GB)

```cpp
# Solution: Reduce packet metadata in mode1.cc (line 468)
pAnim->EnablePacketMetadata(false);
```

## Citation

If you use this simulation in your research, please cite:

```
@misc{uav_mec_simulation_2024,
  title={UAV-Mounted MEC Simulation with Handover Migration Penalty},
  author={[Your Name]},
  year={2024},
  howpublished={NS-3 Implementation}
}
```

## Result

![Simulation Results](images/result.png)

## License

This project is released under the **GNU GPLv2** license (same as NS-3).

## Contact & Support

For questions or issues:

- Open an issue on GitHub
- Email: [bach9747@gmail.com]
- NS-3 Forum: https://www.nsnam.org/support/

## Acknowledgments

- NS-3 Development Team
- LTE-EPC Module Contributors
- NetAnim Visualization Tool

---

**Last Updated**: November 2024  
**NS-3 Version**: 3.43  
**Status**: Production Ready
