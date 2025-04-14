markdown
# Vehicle Trajectory Visualization Tool full version (for TGSIM I90/I94 Stationary Data)

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
```

## Dependencies

- `pandas`
- `plotly`
- `matplotlib`
- `tkinter` (built-in in most Python distributions)

You can install the required packages with:

```bash
pip install pandas plotly matplotlib
```

> `tkinter` is usually included with standard Python installations. If you're using Linux and don't have it installed, try:
>
> ```bash
> sudo apt-get install python3-tk
> ```

## How to Use

1. Launch the Jupyter Notebook (`trajectory_plotter.ipynb`) and run all cells.
2. A GUI window will appear.
3. Select a **run index** to load data.
4. Choose a **time window**, **initial lane**, and **exit lane** (or leave as "all").
5. Select one or more vehicles from the list.
6. Click **Plot** to generate the interactive plot.

The plot will open in a browser window and also be saved as `test_319.html`.

## Update History

- **3/19**: Initial implementation of GUI with lane-changing filtering.
- **3/25**: Fixed bug in lane filtering logic.
- **4/2**: Updated plot range logic for more accurate trajectory visualization.

## Notes

- Centerline CSVs must be named in the format:  
  `I-90-stationary-Run_<run_index>-geometry-with-ramps.csv`
- These files must be placed in the `centerline/` directory relative to the notebook.
- The code currently writes to a fixed output file (`test_319.html`) — feel free to modify this for custom output names.

## License

This project is open-source

## Author

David Feng  
Ph.D. Student, UVA Civil & Environmental Engineering Dept.  <br />
Graduate Research Assistant, Turner-Fairbank Highway Research Center

