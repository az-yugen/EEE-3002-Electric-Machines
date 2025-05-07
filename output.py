import customtkinter as ctk
from panels import *
from settings import *

class Output(ctk.CTkTabview):
    def __init__(self, parent, output_dict):
        super().__init__(master = parent)
        self.grid(row = 0, column = 2, sticky = 'NSEW', padx = 10, pady=10)

        # tabs
        self.add('Output1')
        self.add('Output2')
        self.add('Output3')

        # WIDGETS
        OutputFrame1(self.tab('Output1'), output_dict)
        OutputFrame2(self.tab('Output2'), output_dict)
        OutputFrame3(self.tab('Output3'), output_dict)



class OutputFrame1(ctk.CTkFrame):
    def __init__(self, parent, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        self.output_dict = output_dict    # Store reference to param_dict

        OutputPanel(self, 'Synchronous Speed', output_dict['sync_speed'])
        OutputPanel(self, 'Synchronous Angular Speed', output_dict['sync_rad'])
        OutputPanel(self, 'Armature Resistance', output_dict['arm_res'])
        OutputPanel(self, 'Field Current', output_dict['field_curr'])
        OutputPanel(self, 'OCC Phase Voltage', output_dict['occ_phase_volt'])
        OutputPanel(self, 'SCC Armature Current', output_dict['scc_arm_curr'])
        OutputPanel(self, 'Internal Impedance', output_dict['int_imped'])
        OutputPanel(self, 'Synchronous Reactance', output_dict['sync_react'])


class OutputFrame2(ctk.CTkFrame):
    def __init__(self, parent, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        self.output_dict = output_dict    # Store reference to param_dict

        OutputPanel(self, 'SCC Armature Current', output_dict['scc_arm_curr'])
        OutputPanel(self, 'Armature Current', output_dict['arm_curr'])
        OutputPanel(self, 'Load Angle', output_dict['arm_curr_ang'])
        OutputPanel(self, 'Internal Angle', output_dict['int_ang'])
        OutputPanel(self, 'OCC Phase Voltage', output_dict['occ_phase_volt'])
        OutputPanel(self, 'Internal Voltage', output_dict['int_volt_complex'])
        OutputPanel(self, 'Phase Voltage', output_dict['phase_volt_complex'])
        OutputPanel(self, 'Terminal Voltage', output_dict['term_volt'])
        OutputPanel(self, 'Voltage Regulation', output_dict['volt_reg'])



class OutputFrame3(ctk.CTkFrame):
    def __init__(self, parent, output_dict):
        super().__init__(master = parent)
        self.pack(expand = True, fill = 'both')

        self.output_dict = output_dict    # Store reference to param_dict

        OutputPanel(self, 'Output Power', output_dict['power_out'])
        OutputPanel(self, 'Reactive Power', output_dict['power_out_react'])
        OutputPanel(self, 'Converted Power', output_dict['power_conv'])
        # OutputPanel(self, 'Converted Power2', output_dict['power_conv2'])
        OutputPanel(self, 'Copper Loss', output_dict['power_loss_cu'])
        OutputPanel(self, 'Hysteresis Loss', output_dict['power_loss_he'])
        OutputPanel(self, 'Mechanical Loss', output_dict['power_loss_mech'])
        OutputPanel(self, 'Stray Loss', output_dict['power_loss_stray'])
        OutputPanel(self, 'Input Power', output_dict['power_in'])
        OutputPanel(self, 'Efficiency', output_dict['efficiency'])
        OutputPanel(self, 'Applied Torque', output_dict['torque_app'])
        OutputPanel(self, 'induced Torque', output_dict['torque_ind'])

