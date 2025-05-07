import csv
import numpy as np



def read_csv(file_path):
    """
    Reads a CSV file and returns the data as a list of lists.
    Each inner list represents a row in the CSV file.
    """
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        data = [row for row in reader]
    return data

def write_csv(file_path, data):
    """
    Writes a list of lists to a CSV file.
    Each inner list represents a row in the CSV file.
    """
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data)

def interp():
    """
    Interpolates data from a CSV file and returns the interpolated values.
    """
    # Read the CSV file
    data = read_csv('data_scc1.txt')

    # Convert the data to a NumPy array for easier manipulation
    data_array = np.array(data, dtype=float)

    # Extract the x and y values from the data
    x_values = data_array[:, 0]
    y_values = data_array[:, 1]

    # Perform linear interpolation
    # x_new = np.round(np.arange(np.min(x_values), np.max(x_values)+0.1, 0.1), decimals=2)
    x_new = np.round(np.arange(np.min(x_values), 10, 0.1), decimals=2)
    y_new = np.round(np.interp(x_new, x_values, y_values), decimals=3)

    write_csv('data_scc1_interp.txt', np.column_stack((x_new, y_new)))

    return x_new, y_new


def exterp():
    """
    Extrapolates data from a CSV file and returns the extrapolated values.
    """
    # Read the CSV file
    data = read_csv('data_scc1.txt')

    # Convert the data to a NumPy array for easier manipulation
    data_array = np.array(data, dtype=float)

    # Extract the x and y values from the data
    x_values = data_array[:, 0]
    y_values = data_array[:, 1]

    p = np.polyfit(x_values, y_values, 1)  # Fit a polynomial of degree 1 (linear fit)
    x_new = np.round(np.arange(0, 10, 0.1), decimals=2) # New x values for extrapolation
    y_new = np.round(np.poly1d(p, x_values), decimals=3)  # Evaluate the polynomial at the x values

    # Perform linear extrapolation
    # x_new = np.round(np.arange(np.min(x_values), 10, 0.1), decimals=2)
    # y_new = np.round(np.interp(x_new, x_values, y_values), decimals=3)

    write_csv('data_scc2_exterp.txt', np.column_stack((x_new, y_new)))



# interp()
exterp()