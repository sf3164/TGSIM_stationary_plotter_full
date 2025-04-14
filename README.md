# TGSIM_stationary_plotter
# Vehicle Trajectory Visualization Tool (TGSIM I90/I94 Stationary Data Full version)

This repository contains a Python-based interactive GUI tool for plotting vehicle trajectories from the TGSIM dataset. It allows users to filter vehicles based on simulation run index, time window, and lane-changing behavior, and generates interactive Plotly plots showing detailed movement patterns over road centerlines.

## Features

- Select **run index** from available simulation runs.
- Filter vehicles by **time window**, **initial lane**, and **exit lane**.
- View vehicle **lane change counts** directly in the selection menu.
- Plot interactive **vehicle trajectories** using Plotly with hoverable data points showing:
  - Time
  - Lane
  - Speed
  - Acceleration
- View **lane centerlines** based on corresponding geometry CSVs.

## Example Output

The tool produces an HTML file (`test_319.html`) displaying the interactive plot.

## File Structure

```bash
.
├── TGSIM_Full_Plotting.csv            # Main trajectory dataset
├── centerline/
│   ├── I-90-stationary-Run_1-geometry-with-ramps.csv
│   ├── I-90-stationary-Run_2-geometry-with-ramps.csv
│   └── ...                            # One file per run index
├── trajectory_plotter.ipynb           # Jupyter Notebook with Tkinter GUI and plotting code
└── README.md



