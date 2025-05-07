import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

import numpy as np

from settings import *
from menu import Menu
from plots import Plots
from output import Output




class App(ctk.CTk):
    def __init__(self):

        # WINDOW SETP
        super().__init__()
        self.title('AC Synchronous Machine')
        self.minsize(900, 600)

        # THEME & LAYOUT
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        self.rowconfigure(0, weight = 1, uniform = 'a')
        self.columnconfigure((0,2), weight = 1, uniform = 'a')
        self.columnconfigure(1, weight = 2, uniform = 'a')

        # LOAD INITIAL PARAMETERS
        self.init_parameters()

        # MENU and PLOTS
        Menu(self, self.param_dict, self.output_dict)
        Plots(self, self.param_dict, self.output_dict)
        Output(self, self.output_dict)

        # CLOSE BUTTON
        self.buttonCloseWindow = ctk.CTkButton(self, text='Close Window', command=self.close_window)
        self.buttonCloseWindow.place(relx=0.1, rely=0.9, anchor='sw')


        # INITIATE
        self.mainloop()


    # FUNCTION-INITIAL PARAMETERS
    # ----------------------------------------

    def init_parameters(self):

        # PARAMETER DICTIONARY
        self.param_dict = {
            'poles': ctk.DoubleVar(value = OPTIONS_POLES[0]),
            'freq': ctk.DoubleVar(value = OPTIONS_FREQ[0]),
            'dct_volt': ctk.DoubleVar(value = DEFAULT_DCT_V),
            'dct_curr': ctk.DoubleVar(value = DEFAULT_DCT_C),
            'field_r': ctk.DoubleVar(value = DEFAULT_FIELD_R),
            'field_volt': ctk.DoubleVar(value = DEFAULT_FIELD_V),
            'load_s': ctk.DoubleVar(value = DEFAULT_LOAD_S),
            'load_t': ctk.DoubleVar(value = DEFAULT_LOAD_T)
        }

        self.output_dict = {
            'sync_speed': ctk.DoubleVar(value = 0),
            'sync_rad': ctk.DoubleVar(value = 0),
            'arm_res': ctk.DoubleVar(value = 0.15),
            'field_curr': ctk.DoubleVar(value = 0),
            'occ_phase_volt': ctk.DoubleVar(value = 1000),
            'scc_arm_curr': ctk.DoubleVar(value = 1),
            'int_imped': ctk.DoubleVar(value = 1),
            'sync_react': ctk.DoubleVar(value = 1),
            'arm_curr': ctk.DoubleVar(value = 0),
            'arm_curr_ang': ctk.DoubleVar(value = 0),
            'power_factor': ctk.DoubleVar(value = 0),
            'int_ang': ctk.DoubleVar(value = 0),
            'int_volt_mag': ctk.DoubleVar(value = 1000),
            'int_volt_complex': ctk.StringVar(value = 0),
            'phase_volt_mag': ctk.DoubleVar(value = 1000),
            'phase_volt_complex': ctk.StringVar(value = 1000),
            'term_volt': ctk.DoubleVar(value = 0),
            'volt_reg': ctk.DoubleVar(value = 0),
            'gamma_ang': ctk.DoubleVar(value = 0),
            'power_out': ctk.DoubleVar(value = 0),
            'power_out_react': ctk.DoubleVar(value = 0),
            'power_conv': ctk.DoubleVar(value = 0),
            'power_conv2': ctk.DoubleVar(value = 0),
            'power_loss_cu': ctk.DoubleVar(value = 0),
            'power_loss_he': ctk.DoubleVar(value = 0),
            'power_loss_mech': ctk.DoubleVar(value = 0),
            'power_loss_stray': ctk.DoubleVar(value = 0),
            'power_in': ctk.DoubleVar(value = 0),
            'efficiency': ctk.DoubleVar(value = 0),
            'torque_app': ctk.DoubleVar(value = 0),
            'torque_ind': ctk.DoubleVar(value = 0),
        }

        # for var in self.param_dict.values():
        #     var.trace_add('write', self.update_data)

        # for var in self.output_dict.values():
        #     var.trace_add('write', self.update_data)


        self.param_dict['poles'].trace_add('write', self.calc_speed)
        self.param_dict['poles'].trace_add('write', self.calc_pow_and_tor)
        self.param_dict['freq'].trace_add('write', self.calc_pow_and_tor)
        self.param_dict['freq'].trace_add('write', self.calc_speed)

        self.param_dict['dct_volt'].trace_add('write', self.calc_arm_res)
        self.param_dict['dct_curr'].trace_add('write', self.calc_arm_res)

        self.param_dict['field_r'].trace_add('write', self.calc_field_curr)
        self.param_dict['field_r'].trace_add('write', self.calc_out_volt)

        self.output_dict['occ_phase_volt'].trace_add('write', self.calc_int_imped)
        self.output_dict['scc_arm_curr'].trace_add('write', self.calc_int_imped)

        self.param_dict['load_s'].trace_add('write', self.calc_out_volt)
        self.param_dict['load_t'].trace_add('write', self.calc_out_volt)
        self.output_dict['phase_volt_mag'].trace_add('write', self.calc_field_curr)


        self.output_dict['arm_res'].trace_add('write', self.calc_out_volt)
        self.output_dict['sync_react'].trace_add('write', self.calc_out_volt)
        self.output_dict['occ_phase_volt'].trace_add('write', self.calc_out_volt)

        self.output_dict['arm_curr'].trace_add('write', self.calc_pow_and_tor)
        self.output_dict['arm_curr_ang'].trace_add('write', self.calc_pow_and_tor)
        self.output_dict['int_volt_complex'].trace_add('write', self.calc_pow_and_tor)


        self.update_data()



    # FUNCTIONS - UPDATE DATA
    # ----------------------------------------

    def update_data(self, *args):
        self.calc_speed()
        self.calc_arm_res()
        self.calc_field_curr()
        self.calc_int_imped()
        self.calc_out_volt()
        self.calc_pow_and_tor()


    def calc_speed(self, *args):
        # Calculate synchronous speed and radians
        poles = self.param_dict['poles'].get()
        freq = self.param_dict['freq'].get()

        sync_speed = round((120 * freq) / poles, 2)
        sync_rad = round((2 * np.pi * sync_speed) / 60, 2)

        # Update output dictionary
        self.output_dict['sync_speed'].set(sync_speed)
        self.output_dict['sync_rad'].set(sync_rad)


    def calc_arm_res(self, *args):
        # Calculate armature resistance
        dct_volt = self.param_dict['dct_volt'].get()
        dct_curr = self.param_dict['dct_curr'].get()

        arm_res = round(dct_volt / (2*dct_curr), 2)

        # Update output dictionary
        self.output_dict['arm_res'].set(arm_res)


    def calc_field_curr(self, *args):
        # Calculate field current
        field_r = self.param_dict['field_r'].get()
        field_volt = self.param_dict['field_volt'].get()

        field_curr = round(field_volt / field_r, 2)

        # Update output dictionary
        self.output_dict['field_curr'].set(field_curr)


    def calc_int_imped(self, *args):
        # Calculate internal impedance
        occ_phase_volt = self.output_dict['occ_phase_volt'].get()
        scc_arm_curr = self.output_dict['scc_arm_curr'].get()
        arm_res = self.output_dict['arm_res'].get()

        int_imped = round(occ_phase_volt / scc_arm_curr, 2)
        # sync_react = round(np.sqrt(int_imped**2 - arm_res**2), 2)
        sync_react = 1.1

        # Update output dictionary
        self.output_dict['int_imped'].set(int_imped)
        self.output_dict['sync_react'].set(sync_react)


    # FUNCTION - CALCULATE OUTPUT VOLTAGE
    # ----------------------------------------

    def calc_out_volt(self, *args):
        # Calculate output voltage
        arm_curr = self.param_dict['load_s'].get()
        self.output_dict['arm_curr'].set(arm_curr)
        arm_curr_ang = self.param_dict['load_t'].get()
        self.output_dict['arm_curr_ang'].set(arm_curr_ang)

        arm_res = self.output_dict['arm_res'].get()
        sync_react = self.output_dict['sync_react'].get()

        int_volt_mag = self.output_dict['occ_phase_volt'].get()
        self.output_dict['int_volt_mag'].set(int_volt_mag)

        arm_curr_complex = complex(arm_curr * np.cos(np.radians(arm_curr_ang)), arm_curr * np.sin(np.radians(arm_curr_ang)))
        sync_react_complex = complex(0, sync_react)

        int_ang_rad = np.arcsin( (arm_curr_complex * (arm_res + sync_react_complex)).imag / int_volt_mag )
        int_ang = round(np.degrees(int_ang_rad), 2)

        int_volt_complex = complex(round(int_volt_mag * np.cos(int_ang_rad), 2), round(int_volt_mag * np.sin(int_ang_rad), 2))

        phase_volt_complex = int_volt_complex - arm_curr_complex * (arm_res + sync_react_complex)
        phase_volt_complex = complex(round(phase_volt_complex.real, 2), phase_volt_complex.imag)
        phase_volt_mag = np.abs(phase_volt_complex)

        ter_volt = np.sqrt(3) * phase_volt_mag

        volt_reg = round(100 * (int_volt_mag - phase_volt_mag) / phase_volt_mag, 2)


        # Update output dictionary

        self.output_dict['int_ang'].set(int_ang)
        self.output_dict['int_volt_complex'].set(int_volt_complex)
        self.output_dict['phase_volt_complex'].set(phase_volt_complex)
        self.output_dict['phase_volt_mag'].set(phase_volt_mag)
        self.output_dict['term_volt'].set(ter_volt)
        self.output_dict['volt_reg'].set(volt_reg)



    # FUNCTION - CALCULATE POWER AND TORQUE
    # ----------------------------------------

    def calc_pow_and_tor(self, *args):
        # Calculate output power
        sync_speed = self.output_dict['sync_speed'].get()
        freq = self.param_dict['freq'].get()
        arm_curr = self.output_dict['arm_curr'].get()
        arm_curr_ang = self.output_dict['arm_curr_ang'].get()
        int_ang = self.output_dict['int_ang'].get()
        int_volt_mag = self.output_dict['int_volt_mag'].get()
        phase_volt_mag = self.output_dict['phase_volt_mag'].get()
        arm_res = self.output_dict['arm_res'].get()
        sync_react = self.output_dict['sync_react'].get()
        sync_speed_rad = self.output_dict['sync_rad'].get()

        gamma_ang = round(arm_curr_ang + int_ang, 2)

        power_out = round(3 * phase_volt_mag * arm_curr * np.cos(np.radians(arm_curr_ang)), 2)
        power_out_react = round(3 * phase_volt_mag * arm_curr * np.sin(np.radians(arm_curr_ang)), 2)
        power_conv = round((3 * phase_volt_mag * int_volt_mag * np.sin(np.radians(int_ang)))/sync_react, 2)
        # power_conv2 = round(3 * int_volt_mag * arm_curr * np.cos(np.radians(gamma_ang)), 2)

        power_loss_cu = round(3 * arm_curr * arm_curr * arm_res, 2)
        power_loss_he = round((((freq - 50) / (60-50)) * 1 + 1.5)/100 * power_out, 2)     # varies 1-3% - 1.5 for 50Hz, 2.5 for 60Hz
        power_loss_mech = round((((sync_speed - 500) / (3600 - 500)) * 1.5 + 0.5)/100 * power_out, 2) # varies 0.5-2% - 0.5 for 500rpm, 2 for 3600rpm
        power_loss_stray = round(0.01 * power_out, 2)                                 # constant 1%
        power_loss_tot = power_loss_cu + power_loss_he + power_loss_mech + power_loss_stray

        power_in = round(power_out + power_loss_tot, 2)

        efficiency = round((power_out / power_in) * 100, 2)

        torque_app = round((power_in/sync_speed_rad), 2)
        torque_ind = round((power_conv/sync_speed_rad), 2)

        # Update output dictionary
        self.output_dict['power_out'].set(power_out)
        self.output_dict['power_out_react'].set(power_out_react)
        self.output_dict['power_conv'].set(power_conv)
        # self.output_dict['power_conv2'].set(power_conv2)
        self.output_dict['power_loss_cu'].set(power_loss_cu)
        self.output_dict['power_loss_he'].set(power_loss_he)
        self.output_dict['power_loss_mech'].set(power_loss_mech)
        self.output_dict['power_loss_stray'].set(power_loss_stray)
        self.output_dict['power_in'].set(power_in)
        self.output_dict['efficiency'].set(efficiency)
        self.output_dict['gamma_ang'].set(gamma_ang)
        self.output_dict['torque_app'].set(torque_app)
        self.output_dict['torque_ind'].set(torque_ind)



    # FUNCTION - CLOSE WINDOW
    # ----------------------------------------

    def close_window(self):
        self.withdraw()
        self.quit()




class Calculations:
    def __init__(self, param_dict):
        self.param_dict = param_dict

        # Call the calculation functions
        self.calc_speed()
        self.calc_arm_res()
        self.calc_field_curr()

        # Add more calculations as needed


if __name__ == '__main__':
    App()




# add legend to phasor plot     ✔
# capability curve?
# other losses                  ✔
# latex images
# plot font and colors          ✔
# sankey diagram                ✔
# caution when open circuit
# highlight changes
# add y-delta option
# activate generator button etc
# title and close button