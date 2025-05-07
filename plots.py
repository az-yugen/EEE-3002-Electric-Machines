import customtkinter as ctk
from panels import *
from settings import *

import csv
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

from sankeyflow import Sankey

class Plots(ctk.CTkTabview):
    def __init__(self, parent, param_dict, output_dict, power_dict):
        super().__init__(master = parent)
        self.grid(row = 0, column = 1, rowspan=2, sticky = 'NSEW', padx = 10, pady=10)

        # tabs
        self.add('SCC & OCC')
        self.add('Phasor Diagram')
        self.add('Power Flow')

        # WIDGETS
        CharFrame(self.tab('SCC & OCC'), param_dict, output_dict)
        PhasorFrame(self.tab('Phasor Diagram'), param_dict, output_dict)
        self.sankey_frame = SankeyFrame(self.tab('Power Flow'), power_dict)  # Assign to self.sankey_frame



class CharFrame(ctk.CTkFrame):
    def __init__(self, parent, param_dict, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both', pady = 20, padx = 20)

        self.param_dict = param_dict    # Store reference to param_dict
        self.output_dict = output_dict    # Store reference to param_dict

        # Create Matplotlib figure and axes
        self.fig, self.ax = plt.subplots(1,2, figsize=(8,4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(expand = True, fill = 'both')

        self.fig.patch.set_facecolor('#212121')
        self.fig.patch.set_alpha(1)
        self.ax[0].patch.set_facecolor('#212121')
        self.ax[0].patch.set_alpha(0)
        self.ax[1].patch.set_facecolor('#212121')
        self.ax[1].patch.set_alpha(0)

        # Load data
        self.occ_x, self.occ_y, self.scc_x, self.scc_y = ([] for _ in range(4))
        self.load_data()

        # Initial plot
        self.plot_data()

        # Add trace callback for Load Amount slider
        self.param_dict['field_r'].trace_add('write', self.update_lines)

    def load_data(self):
        # Load OCC data
        with open('data/data_occ0_interp.txt', 'r') as datafile:
            data = csv.reader(datafile, delimiter=',')
            for rows in data:
                self.occ_x.append(float(rows[0]))
                self.occ_y.append(float(rows[1]))

        # Load SCC data
        with open('data/data_scc_interp.txt', 'r') as datafile:
            data = csv.reader(datafile, delimiter=',')
            for rows in data:
                self.scc_x.append(float(rows[0]))
                self.scc_y.append(float(rows[1]))
    

    def plot_data(self):
        # Plot OCC and SCC data
        self.ax[0].plot(self.occ_x, self.occ_y, label='OCC', color='blue')
        self.ax[1].plot(self.scc_x, self.scc_y, label='SCC', color='red')

        # Add grid and labels
        for axis in self.ax:
            axis.grid(color='gray', linestyle='--', linewidth=0.5)
            axis.set_xlabel('X-axis')
            axis.set_ylabel('Y-axis')

        self.canvas.draw()


    def update_lines(self, *args):
        # Get the current value of the Load Amount slider
        field_curr = self.output_dict['field_curr'].get()

        # Find the corresponding y-values for the vertical line
        occ_y_value = self.get_y_value(self.occ_x, self.occ_y, field_curr)
        scc_y_value = self.get_y_value(self.scc_x, self.scc_y, field_curr)

        # SET
        self.output_dict['occ_phase_volt'].set(occ_y_value)
        self.output_dict['scc_arm_curr'].set(scc_y_value)

        # Update or add vertical and horizontal lines to OCC plot
        if hasattr(self, 'occ_vline'):
            self.occ_vline.set_xdata([field_curr, field_curr])
            self.occ_hline.set_ydata([occ_y_value, occ_y_value])
        else:
            self.occ_vline = self.ax[0].axvline(x=field_curr, color='green', linestyle='--', label='Load Amount')
            self.occ_hline = self.ax[0].axhline(y=occ_y_value, color='orange', linestyle='--', label=f'OCC Y={occ_y_value:.2f}')

        # Update or add vertical and horizontal lines to SCC plot
        if hasattr(self, 'scc_vline'):
            self.scc_vline.set_xdata([field_curr, field_curr])
            self.scc_hline.set_ydata([scc_y_value, scc_y_value])
        else:
            self.scc_vline = self.ax[1].axvline(x=field_curr, color='green', linestyle='--', label='Load Amount')
            self.scc_hline = self.ax[1].axhline(y=scc_y_value, color='orange', linestyle='--', label=f'SCC Y={scc_y_value:.2f}')

        # Redraw the canvas
        self.canvas.draw()


    def get_y_value(self, x_data, y_data, x_value):
        # Find the index of the closest x-value
        closest_index = min(range(len(x_data)), key=lambda i: abs(x_data[i] - x_value))

        # Return the corresponding y-value
        return y_data[closest_index]


class PhasorFrame(ctk.CTkFrame):
    def __init__(self, parent, param_dict, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both', pady = 20, padx = 20)

        self.param_dict = param_dict  # Store reference to param_dict
        self.output_dict = output_dict  # Store reference to param_dict

        # --- Matplotlib Figure ---
        fig, self.ax = plt.subplots(figsize=(8,4))
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        fig.patch.set_facecolor('#212121')
        fig.patch.set_alpha(1)

        # Initial draw
        self.draw_phasors()

        # Add trace callbacks to update the plot when sliders change
        self.param_dict['field_r'].trace_add('write', self.on_slider_change)
        self.param_dict['load_s'].trace_add('write', self.on_slider_change)
        self.param_dict['load_t'].trace_add('write', self.on_slider_change)


    # --- Phasor Plotting Function ---
    def draw_phasors(self):
        ax = self.ax
        canvas = self.canvas

        ax.clear()

        # Get updated values from param_dict
        int_volt_mag = self.output_dict['int_volt_mag'].get()
        int_ang = self.output_dict['int_ang'].get()
        arm_curr_mag = self.output_dict['arm_curr'].get()
        arm_curr_ang = self.output_dict['arm_curr_ang'].get()

        arm_res = self.output_dict['arm_res'].get()
        sync_react = self.output_dict['sync_react'].get()

        # Compute phasors
        arm_curr_ang_rad = np.deg2rad(arm_curr_ang)
        arm_curr_complex = arm_curr_mag * np.exp(1j * arm_curr_ang_rad)  # Armature current phasor

        int_ang_rad = np.deg2rad(int_ang)
        int_volt_complex = int_volt_mag * np.exp(1j * int_ang_rad)  # Internal voltage phasor

        vec1 = np.array([int_volt_complex.real, int_volt_complex.imag])
        vec2 = np.array([sync_react * arm_curr_complex.imag, -sync_react * arm_curr_complex.real])
        vec3 = np.array([-arm_res * arm_curr_complex.real, -arm_res * arm_curr_complex.imag])
        vec4 = vec1 + vec2 + vec3

        # Origins
        o1 = np.array([0, 0])
        o2 = o1 + vec1
        o3 = o2 + vec2
        o4 = np.array([0, 0])

        starts = [o1, o2, o3, o4]
        vectors = [vec1, vec2, vec3, vec4]
        colors = ['blue', 'orange', 'red', 'green']
        labels = ['E_A', 'j*X_S*I_A', 'R_A*I_A', 'V_phi']

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
        # ax.set_xlim(x_min, x_max)
        # ax.set_ylim(y_min, y_max)
        ax.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
        ax.yaxis.set_label_position("right")
        ax.set_aspect('equal')
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        ax.set_title(f"E_A:  {np.linalg.norm(vec1):.2f}<{np.rad2deg(np.arctan2(vec1[1], vec1[0])):.1f}°\nV_phi: {np.linalg.norm(vec4):.2f}<{np.rad2deg(np.arctan2(vec4[1], vec4[0])):.1f}°")

        ax.patch.set_facecolor('#212121')
        ax.patch.set_alpha(0)

        canvas.draw()


    # --- Callback for Slider Changes ---
    def on_slider_change(self, *args):
        self.draw_phasors()


class SankeyFrame(ctk.CTkFrame):
    def __init__(self, parent, power_dict):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        self.power_dict = power_dict  # Store reference to power_dict

        # Create initial Sankey diagram
        self.create_sankey()

        # Add Update Button
        self.update_button = ctk.CTkButton(self, text="Update Sankey", command=self.update_sankey)
        self.update_button.pack(pady=10)

    def create_sankey(self):
        # Extract data from power_dict
        sources = self.power_dict['sources']
        targets = self.power_dict['targets']
        values = self.power_dict['values']

        # Create flows as a list of tuples (source, target, value)
        flows = [(src, tgt, val) for src, tgt, val in zip(sources, targets, values)]

        # Create Sankey diagram using SankeyFlow
        fig, ax = plt.subplots(figsize=(8, 6))
        sankey = Sankey(ax=ax, flows=flows)
        sankey.draw()

        # Embed the Matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

        # Close the Matplotlib figure to free memory
        plt.close(fig)

    def update_sankey(self):
        # Clear the existing Sankey diagram and redraw it
        for widget in self.winfo_children():
            if widget != self.update_button:  # Keep the update button
                widget.destroy()
        self.create_sankey()