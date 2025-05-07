import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Phasor Plotting Function ---
def draw_phasors(canvas, ax, L, H_mag, H_angle_deg):
    ax.clear()

    # Compute phasors
    H_angle_rad = np.deg2rad(H_angle_deg)
    H = H_mag * np.exp(1j * H_angle_rad)

    vec1 = np.array([L, 0])                          # Green
    vec2 = np.array([2 * H.real, 2 * H.imag])        # Red = 2H
    vec3 = np.array([-5 * H.imag, 5 * H.real])       # Orange = 5jH
    vec4 = vec1 + vec2 + vec3                        # Blue = Resultant

    # Origins
    o1 = np.array([0, 0])
    o2 = o1 + vec1
    o3 = o2 + vec2
    o4 = o1

    starts = [o1, o2, o3, o4]
    vectors = [vec1, vec2, vec3, vec4]
    colors = ['green', 'red', 'orange', 'blue']
    labels = ['Green (L)', 'Red (2H)', 'Orange (5jH)', 'Resultant']

    all_points = []

    for start, vec, color, label in zip(starts, vectors, colors, labels):
        end = start + vec
        ax.arrow(start[0], start[1], vec[0], vec[1],
                 head_width=0.2, head_length=0.3, fc=color, ec=color, length_includes_head=True)
        ax.text(end[0], end[1], label, fontsize=9, color=color)
        all_points.extend([start, end])

    all_points = np.array(all_points)
    x_min, x_max = all_points[:, 0].min() - 2, all_points[:, 0].max() + 2
    y_min, y_max = all_points[:, 1].min() - 2, all_points[:, 1].max() + 2
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title(f"Resultant Magnitude: {np.linalg.norm(vec4):.2f}, Angle: {np.rad2deg(np.arctan2(vec4[1], vec4[0])):.1f}°")

    canvas.draw()

# --- GUI Setup ---
root = tk.Tk()
root.title("Phasor Visualizer (Tkinter + Matplotlib)")

# --- Matplotlib Figure ---
fig, ax = plt.subplots(figsize=(6, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# --- Control Frame ---
def on_slider_change(_=None):
    draw_phasors(canvas, ax,
                 L_var.get(),
                 H_mag_var.get(),
                 H_angle_var.get())

L_var = tk.DoubleVar(value=5.0)
H_mag_var = tk.DoubleVar(value=1.0)
H_angle_var = tk.DoubleVar(value=0.0)

ttk.Label(root, text="Green Vector Magnitude (L)").grid(row=1, column=0)
L_slider = ttk.Scale(root, from_=0.1, to=10.0, variable=L_var, orient='horizontal', command=on_slider_change)
L_slider.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

ttk.Label(root, text="H Magnitude").grid(row=1, column=1)
H_mag_slider = ttk.Scale(root, from_=0.1, to=5.0, variable=H_mag_var, orient='horizontal', command=on_slider_change)
H_mag_slider.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

ttk.Label(root, text="H Angle (degrees)").grid(row=1, column=2)
H_angle_slider = ttk.Scale(root, from_=-180, to=180, variable=H_angle_var, orient='horizontal', command=on_slider_change)
H_angle_slider.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

# Initial draw
draw_phasors(canvas, ax, L_var.get(), H_mag_var.get(), H_angle_var.get())

# Start GUI loop
root.mainloop()
