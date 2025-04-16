import pandas as pd
import plotly.graph_objects as go
import os
import matplotlib.colors as mcolors
import tkinter as tk
from tkinter import ttk, messagebox

# File Paths
TRAJECTORY_FILE = "TGSIM_Stationary.csv"
CENTERLINE_FOLDER = "centerline"

# Load trajectory data
traj_df = pd.read_csv(TRAJECTORY_FILE)

# Initialize main Tkinter window
root = tk.Tk()
root.title("Vehicle Trajectory Plotter")

# Global variables to store user selections
selected_run = tk.StringVar()
selected_time = tk.StringVar()
selected_initial_lane = tk.StringVar()
selected_exit_lane = tk.StringVar()

def update_time_options(*args):
    """ Updates time window options based on the selected run index """
    try:
        run_index = int(selected_run.get())
        run_data = traj_df[traj_df["run_index"] == run_index]

        if run_data.empty:
            messagebox.showerror("Error", "No data available for this run.")
            return
        
        min_time = int(run_data["time"].min())
        max_time = int(run_data["time"].max())

        # Generate 60-second time windows to shorten vehicle list
        time_windows = ["all"] + [f"{t}-{t+60}" for t in range(min_time, max_time, 60)]
        time_menu["values"] = time_windows
        selected_time.set("")

        # Update initial and exit lane dropdowns
        unique_lanes = sorted(run_data["lane_kf"].dropna().unique().astype(int))
        lane_options = ["all"] + [str(lane) for lane in unique_lanes]
        initial_lane_menu["values"] = lane_options
        exit_lane_menu["values"] = lane_options
        selected_initial_lane.set("all")
        selected_exit_lane.set("all")

    except ValueError:
        messagebox.showerror("Error", "Invalid run index selection.")

def update_vehicle_options(*args):
    """Updates vehicle options based on selected time window and initial/exit lane filters"""
    try:
        run_index = int(selected_run.get())
        time_window = selected_time.get()

        run_data = traj_df[traj_df["run_index"] == run_index]

        # Step 1: Identify vehicles appearing within the selected time range
        if time_window != "all":
            start_time, end_time = map(int, time_window.split("-"))
            vehicles_in_time_range = run_data[
                (run_data["time"] >= start_time) & (run_data["time"] <= end_time)
            ]["id"].unique()
        else:
            vehicles_in_time_range = run_data["id"].unique()

        # Step 2: Fetch full trajectories (ignoring time filter) for these vehicles
        full_traj_data = traj_df[
            (traj_df["run_index"] == run_index) & (traj_df["id"].isin(vehicles_in_time_range))
        ].sort_values(["id", "time"])

        # Step 3: Extract initial and exit lanes from entire trajectories
        first_last_lanes = full_traj_data.groupby("id").agg(
            initial_lane=("lane_kf", "first"),
            exit_lane=("lane_kf", "last"),
            lane_changes=("lane_kf", lambda x: (x.diff().fillna(0) != 0).sum())
        ).reset_index()

        # Step 4: Apply user-selected initial and exit lane filters
        initial_lane_filter = selected_initial_lane.get()
        exit_lane_filter = selected_exit_lane.get()

        if initial_lane_filter != "all":
            initial_lane_filter = int(initial_lane_filter)
            first_last_lanes = first_last_lanes[first_last_lanes["initial_lane"] == initial_lane_filter]

        if exit_lane_filter != "all":
            exit_lane_filter = int(exit_lane_filter)
            first_last_lanes = first_last_lanes[first_last_lanes["exit_lane"] == exit_lane_filter]

        # Step 5: Populate the vehicle listbox with final filtered vehicles
        vehicle_listbox.delete(0, tk.END)
        for _, row in first_last_lanes.iterrows():
            vid = int(row["id"])
            lane_change_count = int(row["lane_changes"])
            vehicle_listbox.insert(tk.END, f"{vid} ({lane_change_count} lane changes)")

    except ValueError:
        messagebox.showerror("Error", "Invalid selection.")




def plot_trajectories():
    """ Plots the selected vehicle trajectories using Plotly """
    try:
        run_index = int(selected_run.get())
        time_window = selected_time.get()

        # Extract selected vehicle IDs from listbox
        selected_indices = vehicle_listbox.curselection()
        selected_vehicle_ids = [int(vehicle_listbox.get(i).split()[0]) for i in selected_indices]  # Extract ID only

        if not selected_vehicle_ids:
            messagebox.showerror("Error", "No vehicles selected.")
            return

        # Compute the max ranges
        max_x = traj_df[(traj_df["run_index"] == run_index)]['xloc_kf'].max()
        max_y = traj_df[(traj_df["run_index"] == run_index)]['yloc_kf'].max()
        
        # Get full trajectory of these vehicles (no time filtering for plotting)
        filtered_traj = traj_df[(traj_df["run_index"] == run_index) & (traj_df["id"].isin(selected_vehicle_ids))]

        # Find only the lanes traveled by these selected vehicles
        traveled_lanes = filtered_traj["lane_kf"].dropna().unique()

        # Load centerline data
        centerline_file = os.path.join(CENTERLINE_FOLDER, f"I-90-stationary-Run_{run_index}-geometry-with-ramps.csv")
        if not os.path.exists(centerline_file):
            messagebox.showerror("Error", f"Centerline file not found: {centerline_file}")
            return
        
        centerline_df = pd.read_csv(centerline_file)

        # Assign colors to each vehicle
        color_list = list(mcolors.TABLEAU_COLORS.values())
        vehicle_color_map = {vid: color_list[i % len(color_list)] for i, vid in enumerate(selected_vehicle_ids)}

        # Create a Plotly figure
        fig = go.Figure()



        # Plot only the lanes that the selected vehicles traveled on
        # **Plot all lanes, not just traveled lanes**
        for lane in centerline_df.columns:
            if lane.startswith("x_"):  # Identify lane columns
                lane_number = lane.split("_")[1]  # Extract lane ID
                lane_centerline_column_x = f"x_{lane_number}"
                lane_centerline_column_y = f"y_{lane_number}"
                
                if lane_centerline_column_x in centerline_df.columns and lane_centerline_column_y in centerline_df.columns:
                    lane_centerline = centerline_df[[lane_centerline_column_x, lane_centerline_column_y]].dropna()
        
                    fig.add_trace(go.Scatter(
                        x=lane_centerline.iloc[:, 0], 
                        y=lane_centerline.iloc[:, 1], 
                        mode="lines", 
                        line=dict(color="#D3D3D3", width=1.5),
                        name=f"Lane {lane_number}"
                    ))
        
                    # Add lane ID label at the end of the centerline
                    end_x, end_y = lane_centerline.iloc[-1, 0], lane_centerline.iloc[-1, 1]
                    fig.add_trace(go.Scatter(
                        x=[end_x], 
                        y=[end_y], 
                        mode="text", 
                        text=[f"Lane {lane_number}"], 
                        textposition="top right",
                        showlegend=False
                    ))

        # Plot vehicle trajectories with hover info
        # Plot vehicle trajectories with hover info including time, lane, speed, and acceleration
        for vehicle_id in selected_vehicle_ids:
            vehicle_data = filtered_traj[filtered_traj["id"] == vehicle_id]
            if not vehicle_data.empty:
                hover_texts = [
                    f"ID:{vehicle_id}<br>Time: {t}s<br>Lane: {int(lane)}<br>Speed: {speed:.2f} m/s<br>Acceleration: {accel:.2f} m/s²"
                    for t, lane, speed, accel in zip(vehicle_data["time"], 
                                                     vehicle_data["lane_kf"], 
                                                     vehicle_data["speed_kf"], 
                                                     vehicle_data["acceleration_kf"])
                ]
        
                fig.add_trace(go.Scatter(
                    x=vehicle_data["xloc_kf"], 
                    y=vehicle_data["yloc_kf"], 
                    mode="markers",
                    marker=dict(size=5),
                    line=dict(color=vehicle_color_map[vehicle_id], width=2),
                    name=f"Vehicle {vehicle_id}",
                    text=hover_texts,
                    hoverinfo="text+x+y"
                ))


        # Formatting
        fig.update_layout(
            title=f"Vehicle Trajectories for Run {run_index}",
            xaxis=dict(range=[0, max_x]),
            yaxis=dict(range=[0, max_y]),
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
            legend_title="Legend",
            template="plotly_white"
        )

        fig.write_html("Stationary_Full_Plot.html")
        # Show the interactive Plotly plot
        fig.show()
        fig.show()

    except ValueError:
        messagebox.showerror("Error", "Invalid vehicle selection.")

# Create Tkinter UI elements
tk.Label(root, text="Select Run Index:").grid(row=0, column=0)
run_options = traj_df["run_index"].unique().tolist()
run_menu = ttk.Combobox(root, textvariable=selected_run, values=[str(int(run)) for run in run_options], state="readonly")
run_menu.grid(row=0, column=1)
run_menu.bind("<<ComboboxSelected>>", update_time_options)

tk.Label(root, text="Select Time Window:").grid(row=1, column=0)
time_menu = ttk.Combobox(root, textvariable=selected_time, state="readonly")
time_menu.grid(row=1, column=1)
time_menu.bind("<<ComboboxSelected>>", update_vehicle_options)

tk.Label(root, text="Initial Lane:").grid(row=2, column=0)
initial_lane_menu = ttk.Combobox(root, textvariable=selected_initial_lane, state="readonly")
initial_lane_menu.grid(row=2, column=1)
initial_lane_menu.bind("<<ComboboxSelected>>", update_vehicle_options)  

tk.Label(root, text="Exit Lane:").grid(row=3, column=0)
exit_lane_menu = ttk.Combobox(root, textvariable=selected_exit_lane, state="readonly")
exit_lane_menu.grid(row=3, column=1)
exit_lane_menu.bind("<<ComboboxSelected>>", update_vehicle_options)  

tk.Label(root, text="Select Vehicles:").grid(row=4, column=0)
vehicle_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10)
vehicle_listbox.grid(row=4, column=1)

tk.Button(root, text="Plot", command=plot_trajectories).grid(row=5, column=0, columnspan=2)


root.mainloop()
