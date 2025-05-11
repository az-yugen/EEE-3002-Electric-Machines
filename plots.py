import customtkinter as ctk
from panels import *
from settings import *
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import EngFormatter
import numpy as np
from sankeyflow import Sankey
from engineering_notation import EngNumber
import scienceplots



class Plots(ctk.CTkTabview):
    def __init__(self, parent, param_dict, output_dict):
        super().__init__(master = parent)
        self.grid(row = 0, column = 1, rowspan=2, sticky = 'NSEW', pady=10)

        # TABS
        self.add('OCC & SCC')
        self.add('Phasor Diagram')
        self.add('Power Flow')
        # self.add('Capability Curve')

        # plt.style.use(['dark_background','science','ieee'])
        plt.style.use('dark_background')

        # WIDGETS
        CharFrame(self.tab('OCC & SCC'), param_dict, output_dict)
        PhasorFrame(self.tab('Phasor Diagram'), param_dict, output_dict)
        SankeyFrame(self.tab('Power Flow'), output_dict)



class CharFrame(ctk.CTkFrame):
    def __init__(self, parent, param_dict, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both', pady = 5, padx = 5)

        self.param_dict = param_dict    # Store reference to param_dict
        self.output_dict = output_dict    # Store reference to param_dict
        self.field_curr = self.output_dict['field_curr'].get()

        # Create Matplotlib figure and axes
        self.fig, self.ax = plt.subplots(2,1, figsize=(6,6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(expand = True, fill = 'both')
        self.fig.subplots_adjust(left =0.15, right=0.75, top=0.95, hspace=0)
        self.fig.patch.set_facecolor('#212121')
        self.fig.patch.set_alpha(1)
        plt.suptitle('OCC & SCC\n', x=1.1, y=0.5, fontsize=14, weight='bold', color='white')

        # Load data
        self.occ_x, self.occ_y, self.occ_ag_x, self.occ_ag_y, self.scc_x, self.scc_y = ([] for i in range(6))
        self.load_data()

        # Initial plot
        self.plot_data()

        self.param_dict['field_r'].trace_add('write', self.update_lines)

    def load_data(self):
        # Load OCC data
        with open('data/p52_occ_interp.txt', 'r') as datafile:
            data = csv.reader(datafile, delimiter=',')
            for rows in data:
                self.occ_x.append(float(rows[0]))
                self.occ_y.append(float(rows[1]))

        # Load OCC data with airgap line
        with open('data/p52_ag_occ_interp.txt', 'r') as datafile:
            data = csv.reader(datafile, delimiter=',')
            for rows in data:
                self.occ_ag_x.append(float(rows[0]))
                self.occ_ag_y.append(float(rows[1]))


        # Load SCC data
        with open('data/p52_scc_interp.txt', 'r') as datafile:
            data = csv.reader(datafile, delimiter=',')
            for rows in data:
                self.scc_x.append(float(rows[0]))
                self.scc_y.append(float(rows[1]))
    

    def plot_data(self):
        # Plot OCC, OCC_AG and SCC data
        self.ax[0].plot(self.occ_ag_x, self.occ_ag_y, label='OCC_AG', color='mediumseagreen', linestyle='--')
        self.ax[0].plot(self.occ_x, self.occ_y, label='OCC', color='dodgerblue')
        self.ax[1].plot(self.scc_x, self.scc_y, label='SCC', color='orangered')

        # Add grid and labels
        for axis in self.ax:
            axis.grid(color='gray', linestyle='--', linewidth=0.5)
            axis.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
            axis.patch.set_facecolor('#212121')
            axis.patch.set_alpha(0)

        self.ax[0].set_ylabel('Open Circuit Terminal Voltage (V)')
        self.ax[1].set_ylabel('Short Circuit Armature Current (A)')
        self.ax[1].set_xlabel('Field Current (A)')
        self.ax[0].xaxis.set_ticklabels([])
        yaxis_format = EngFormatter(places=0, sep="\N{THIN SPACE}")
        # self.ax[0].yaxis.set_major_formatter(yaxis_format)
        # self.ax[1].yaxis.set_major_formatter(yaxis_format)
        # self.ax[1].yaxis.tick_right()
        # self.ax[1].yaxis.set_label_position("right")

        x_min, x_max = min(self.occ_x), max(self.occ_x)
        y_min, y_max = min(self.occ_y), max(self.occ_y)
        self.ax[0].set_xlim(x_min, x_max)
        self.ax[1].set_xlim(x_min, x_max)
        self.ax[0].set_ylim(y_min, y_max)

        self.canvas.draw()


    def update_lines(self, *args):
        self.field_curr = self.output_dict['field_curr'].get()

        # Find the corresponding y-values for the vertical line
        self.occ_y_value = self.get_y_value(self.occ_x, self.occ_y, self.field_curr)
        self.occ_ag_y_value = self.get_y_value(self.occ_ag_x, self.occ_ag_y, self.field_curr)
        self.scc_y_value = self.get_y_value(self.scc_x, self.scc_y, self.field_curr)

        # SET
        self.output_dict['occ_term_volt'].set(self.occ_y_value)
        self.output_dict['occ_ag_term_volt'].set(self.occ_ag_y_value)
        self.output_dict['scc_arm_curr'].set(self.scc_y_value)

        # Update or add vertical and horizontal lines to OCC plot
        if hasattr(self, 'occ_vline'):
            self.occ_vline.set_xdata([self.field_curr, self.field_curr])
            self.occ_hline.set_ydata([self.occ_y_value, self.occ_y_value])
        else:
            self.occ_vline = self.ax[0].axvline(x=self.field_curr, color='lavender', alpha=0.5, linestyle='--', label='Load Amount')
            self.occ_hline = self.ax[0].axhline(y=self.occ_y_value, color='lavender', alpha=0.5, linestyle='--', label=f'OCC Y={self.occ_y_value:.2f}')

        # Update or add vertical and horizontal lines to SCC plot
        if hasattr(self, 'scc_vline'):
            self.scc_vline.set_xdata([self.field_curr, self.field_curr])
            self.scc_hline.set_ydata([self.scc_y_value, self.scc_y_value])
        else:
            self.scc_vline = self.ax[1].axvline(x=self.field_curr, color='lavender', alpha=0.5, linestyle='--', label='Load Amount')
            self.scc_hline = self.ax[1].axhline(y=self.scc_y_value, color='lavender', alpha=0.5, linestyle='--', label=f'SCC Y={self.scc_y_value:.2f}')

        label_vtoc = '$V_{T, OC}$'
        label_iasc = '$I_{A, SC}$'
        self.ax[0].set_title(f'{label_vtoc} = {self.occ_y_value} V \n\n $I_F = ${self.field_curr} A', x=1.2, y=0, fontsize=14, weight='bold', color='white')
        self.ax[1].set_title(f'{label_iasc} = {self.scc_y_value} A \n', x=1.2, y=0.8, fontsize=14, weight='bold', color='white')

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
        self.pack(expand = True, fill = 'both', pady = 5, padx = 5)

        self.param_dict = param_dict  # Store reference to param_dict
        self.output_dict = output_dict  # Store reference to param_dict

        # --- Matplotlib Figure ---
        fig, self.ax = plt.subplots(figsize=(6,6))
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(expand = True, fill = 'both')

        fig.patch.set_facecolor('#212121')
        fig.patch.set_alpha(1)
        fig.subplots_adjust(right=0.85)

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
        sync_react_sat = self.output_dict['sync_react_sat'].get()

        # Compute phasors
        arm_curr_ang_rad = np.deg2rad(arm_curr_ang)
        arm_curr_complex = arm_curr_mag * np.exp(1j * arm_curr_ang_rad)  # Armature current phasor

        int_ang_rad = np.deg2rad(int_ang)
        int_volt_complex = int_volt_mag * np.exp(1j * int_ang_rad)  # Internal voltage phasor

        vec1 = np.array([int_volt_complex.real, int_volt_complex.imag])
        vec2 = np.array([sync_react_sat * arm_curr_complex.imag, -sync_react_sat * arm_curr_complex.real])
        vec3 = np.array([-arm_res * arm_curr_complex.real, -arm_res * arm_curr_complex.imag])
        vec4 = vec1 + vec2 + vec3
        vec5 = np.array([arm_curr_complex.real, arm_curr_complex.imag])

        # Origins
        o1 = np.array([0, 0])
        o2 = o1 + vec1
        o3 = o2 + vec2
        o4 = np.array([0, 0])
        o5 = np.array([0, 0])

        starts = [o1, o2, o3, o4, o5]
        vectors = [vec1, vec2, vec3, vec4, vec5]
        colors = ['dodgerblue', 'gold', 'orangered', 'mediumseagreen', 'lavender']
        labels = ['$E_A$', '$jX_SI_A$', '$R_AI_A$', '$V_{\phi}$', '$I_A$']

        all_points = []
        # legend_entries = []

        for start, vec, color, label in zip(starts, vectors, colors, labels):
            end = start + vec
            mid = (start + end) / 2
            ax.arrow(start[0], start[1], vec[0], vec[1],
                    width=0.5, head_width=0.2, head_length=0.3, fc=color, ec=color, length_includes_head=True)
            # ax.text(mid[0], mid[1], label, fontsize=9, color=color)

            # Add legend entry with magnitude and angle
            magnitude = np.linalg.norm(vec)
            angle = np.rad2deg(np.arctan2(vec[1], vec[0]))
            ax.text(mid[0], mid[1], f"{label}\n{magnitude:.2f}∠{angle:.1f}°",
                    fontsize=11, weight='bold', color=color, ha='left', va='bottom')
            # legend_entries.append(f"{label}: {magnitude:.2f}∠{angle:.1f}°")

            all_points.extend([start, end])

        all_points = np.array(all_points)
        # Add legend to the plot
        # ax.legend(
        #     handles=[
        #         plt.Line2D([0], [0], color=color, lw=2, label=entry)
        #         for color, entry in zip(colors, legend_entries)
        #     ],
        #     loc='upper left',
        #     fontsize=9,
        #     frameon=False
        # )
        
        # x_min, x_max = all_points[:, 0].min() - 2, all_points[:, 0].max() + 2
        # y_min, y_max = all_points[:, 1].min() - 2, all_points[:, 1].max() + 2
        # ax.set_xlim(x_min, x_max)
        # ax.set_ylim(y_min, y_max)
        ax.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.yaxis.set_label_position("right")
        ax.set_aspect('equal')
        ax.grid(color='gray', linestyle='--', linewidth=0.5)
        # ax.set_title(f"{labels[0]}:  {np.linalg.norm(vec1):.2f}<{np.rad2deg(np.arctan2(vec1[1], vec1[0])):.1f}°\n"
        #              f"{labels[3]}: {np.linalg.norm(vec4):.2f}<{np.rad2deg(np.arctan2(vec4[1], vec4[0])):.1f}°")
        ax.set_title('Phasor Diagram', fontsize=14, weight='bold', color='white')

        ax.patch.set_facecolor('#212121')
        ax.patch.set_alpha(0)

        canvas.draw()



    # --- Callback for Slider Changes ---
    def on_slider_change(self, *args):
        self.draw_phasors()









class SankeyFrame(ctk.CTkFrame):
    def __init__(self, parent, output_dict):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        self.output_dict = output_dict  # Store reference to output_dict

        # Create initial Sankey diagram
        # self.create_sankey()

        # Add Update Button
        self.update_button = ctk.CTkButton(self, text="Update Sankey", command=self.update_sankey)
        self.update_button.pack(pady=10)

    def create_sankey(self):

        # Extract data from output_dict
        # nodes = [
        #     [('Input Power', self.output_dict['power_in'].get())],
        #     [('Converted Power', self.output_dict['power_conv'].get()),
        #      ('Mechanical Loss', self.output_dict['power_loss_mech'].get()),
        #      ('Core Loss',self.output_dict['power_loss_he'].get()),
        #      ('Stray Loss', self.output_dict['power_loss_stray'].get())],
        #     [('Output Power', self.output_dict['power_out'].get()),
        #      ('Copper Loss', self.output_dict['power_loss_cu'].get())],
        # ]

        # flows = [
        #     ('Input Power', 'Converted Power', self.output_dict['power_conv'].get()),
        #     ('Converted Power', 'Output Power', self.output_dict['power_out'].get()),
        #     ('Converted Power', 'Copper Loss', self.output_dict['power_loss_cu'].get()),
        #     ('Input Power', 'Core Loss', self.output_dict['power_loss_he'].get()),
        #     ('Input Power', 'Mechanical Loss', self.output_dict['power_loss_mech'].get()),
        #     ('Input Power', 'Stray Loss', self.output_dict['power_loss_stray'].get()),
        # ]

        nodes = [
            [('Input Power', self.output_dict['power_in'].get())],
            [('Output Power', self.output_dict['power_out'].get()),
             ('Copper Loss', self.output_dict['power_loss_cu'].get()),
             ('Core Loss',self.output_dict['power_loss_he'].get()),
             ('Mechanical Loss', self.output_dict['power_loss_mech'].get()),
             ('Stray Loss', self.output_dict['power_loss_stray'].get())],
        ]

        flows = [
            ('Input Power', 'Output Power', self.output_dict['power_out'].get()),
            ('Input Power', 'Copper Loss', self.output_dict['power_loss_cu'].get()),
            ('Input Power', 'Core Loss', self.output_dict['power_loss_he'].get()),
            ('Input Power', 'Mechanical Loss', self.output_dict['power_loss_mech'].get()),
            ('Input Power', 'Stray Loss', self.output_dict['power_loss_stray'].get()),
        ]

        # Create Sankey diagram using SankeyFlow
        fig, ax = plt.subplots(figsize=(6, 6))
        # plt.rcParams.update({'font.size': 8})
        plt.subplots_adjust(left=0.3)


        fig.patch.set_facecolor('#212121')
        fig.patch.set_alpha(1)

        # s = Sankey(flows=flows, nodes=nodes, node_opts=dict(label_format='{label} {value:.2f}W'),)
        s = Sankey(flows=flows, nodes=nodes, node_opts=dict(label_format='{label}: {value:,.0f}W'),)
        s.draw()

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