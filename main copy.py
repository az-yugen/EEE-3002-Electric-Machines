import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

import numpy as np

import csv

from settings import *
from menu import Menu

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class App(ctk.CTk):
    def __init__(self):

        # WINDOW SETP
        super().__init__()
        self.title('Project')
        self.geometry('1100x700')
        self.resizable(False, False)


        # LAYOUT
        self.columnconfigure((0,1,2), weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure((1,2), weight = 3, uniform = 'a')


        # CLOSE BUTTON
        self.buttonCloseWindow = ctk.CTkButton(self, text='Close Window', command=self.close_window)
        self.buttonCloseWindow.grid(row=0,column=2)


        # WIDGETS

        QuantitiesFrame(self)

        

        self.create_widgets()



        self.init_parameters()

        # OCC graph
        # self.plot_occ(1,0, (4,4))
        # SCC graph
        # self.plot_scc(2,0, (4,4))
        # phasor graph
        # self.plot_phasor(1,2, (6,4))

        # RUN
        self.mainloop()


    # FUNCTIONS

    def init_parameters(self):

        self.param_dict = {
            'poles': ctk.DoubleVar(value = OPTIONS_POLES[0]),
            'freq': ctk.DoubleVar(value = OPTIONS_FREQ[0]),
            'dct_volt': ctk.DoubleVar(value = DEFAULT_DCT_V),
            'dct_curr': ctk.DoubleVar(value = DEFAULT_DCT_C),
            'field_r': ctk.DoubleVar(value = DEFAULT_FIELD_R),
            'load_s': ctk.DoubleVar(value = DEFAULT_LOAD_S),
            'load_t': ctk.DoubleVar(value = DEFAULT_LOAD_T)
        }

        Menu(self, self.param_dict)
        

    def close_window(self):
        self.withdraw()
        self.quit()

    def create_widgets(self):

        label1 = ctk.CTkLabel(self, text = 'Label 1', bg_color = 'red')
        label2 = ctk.CTkLabel(self, text = 'Label 2', bg_color = 'red')
        label3 = ctk.CTkLabel(self, text = 'Label 3', bg_color = 'red')
        
        label1.grid(row = 0, column = 1)
        label3.grid(row = 2, column = 1)


    def create_plots(self, row, col, figsize):
        fig, ax = plt.subplots(figsize=(figsize[0], figsize[1]))

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(row=row, column=col)

        fig.patch.set_facecolor('#242424')
        fig.patch.set_alpha(1)


        ax.patch.set_facecolor('#242424')
        ax.patch.set_alpha(0)

        return ax, canvas

    def plot_occ(self, row, col, figsize):
        ax, canvas = self.create_plots(row, col, figsize)
        X = []
        Y = []
        with open('data_occ.txt', 'r') as datafile:
            data = csv.reader(datafile, delimiter=',')
            for rows in data:
                X.append(float(rows[0]))
                Y.append(float(rows[1]))
        ax.plot(X, Y)
        canvas.draw()

    def plot_scc(self, row, col, figsize):
        ax, canvas = self.create_plots(row, col, figsize)
        X = []
        Y = []
        with open('data_scc.txt', 'r') as datafile:
            data = csv.reader(datafile, delimiter=',')
            for rows in data:
                X.append(float(rows[0]))
                Y.append(float(rows[1]))
        ax.plot(X, Y)
        canvas.draw()

    def plot_phasor(self, row, col, figsize):

        ax, canvas = self.create_plots(row, col, figsize)

        x = np.random.randint(0, 10, 10)
        y = np.random.randint(0, 10, 10)
        ax.scatter(x, y)
        canvas.draw()



class QuantitiesFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.grid(row = 1, column=1, ipady = 15)

        # LAYOUT
        self.rowconfigure((0,1,2,3,4), weight=1, uniform = 'b')
        self.columnconfigure(0, weight=1, uniform='b')
        self.columnconfigure(1, weight=2, uniform='b')
        self.columnconfigure(2, weight=1, uniform='b')

        # TEXT
        font = ctk.CTkFont(family = FONT, size = LABEL_FONT_SIZE, weight='bold')
        label_speed = ctk.CTkLabel(self, text = 'SPEED\t:', text_color= WHITE, font = font, bg_color=BLACK)
        label_dctest = ctk.CTkLabel(self, text = 'DC TEST\t:', text_color= WHITE, font = font, bg_color=BLACK)
        label_field_r = ctk.CTkLabel(self, text = 'FIELD R\t:', text_color= WHITE, font = font, bg_color=BLACK)
        label_load_s = ctk.CTkLabel(self, text = 'LOAD SIZE :', text_color= WHITE, font = font, bg_color=BLACK)
        label_load_t = ctk.CTkLabel(self, text = 'LOAD TYPE :', text_color= WHITE, font = font, bg_color=BLACK)
        label_speed.grid(row=0, column=0, sticky= 'e')
        label_dctest.grid(row=1, column=0, sticky= 'e')
        label_field_r.grid(row=2, column=0, sticky= 'e')
        label_load_s.grid(row=3, column=0, sticky= 'e')
        label_load_t.grid(row=4, column=0, sticky= 'e')


        # INPUTS
        inp_pole = ctk.CTkEntry(self, placeholder_text='Pole')
        inp_freq = ctk.CTkEntry(self, placeholder_text='Frequency')
        inp_dct_v = ctk.CTkEntry(self, placeholder_text='DC volt')
        inp_dct_i = ctk.CTkEntry(self, placeholder_text='DC I')

        inp_pole.grid(row = 0, column = 1)
        inp_freq.grid(row = 0, column = 1)
        inp_dct_v.grid(row = 1, column = 1)
        inp_dct_i.grid(row = 1, column = 1)

        # SLIDERS
        slider_field_r = ctk.CTkSlider(self)
        slider_load_s = ctk.CTkSlider(self)
        slider_load_t = ctk.CTkSlider(self)
        slider_field_r.grid(row=2, column=1)
        slider_load_s.grid(row=3, column=1)
        slider_load_t.grid(row=4, column=1)


if __name__ == '__main__':
    App()