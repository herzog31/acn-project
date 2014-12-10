'''
Created on 09.12.2014
ACN Project
Plotter

@author: Group 19
'''
import argparse
from matplotlib import pyplot


def create_boxplot_figure(ftp_measurement, http_measurement, ssh_measurement):
    '''
    Reads the input files (which may be None) and plots the results.
    If None is passed, nothing will be plotted for that protocol.
    Returns a figure containing the box-plot.
    '''
    # List of value-lists for the three protocols
    values_to_plot = []

    # List of protocol labels
    labels = []

    # Check for all three lists
    # Append the list of results from one protocol to the list of value-lists

    if ftp_measurement is not None and ftp_measurement:
        values_to_plot.append(ftp_measurement)
        labels.append("FTP")

    if http_measurement is not None and http_measurement:
        values_to_plot.append(http_measurement)
        labels.append("HTTP")

    if ssh_measurement is not None and ssh_measurement:
        values_to_plot.append(ssh_measurement)
        labels.append("SSH")

    # Create one plot-figure
    fig = pyplot.figure(1, figsize=(9, 6))

    # Add values to the figure and create the box-plot
    ax = fig.add_subplot(111)
    ax.boxplot(values_to_plot)
    # Set the labels of the x-axis
    ax.set_xticklabels(labels)

    return fig


def save_plot_to_file(fig, filename):
    '''
    Stores the plot into the file.
    If None is passed this function does nothing.
    '''
    # Do nothing if no file is specified
    if filename is None:
        return

    # Nothing to store if fig is None
    if fig is None:
        return

    # Save the figure to file; the extensions determines the file-type
    fig.savefig(filename)


def read_values_from_file(filename):
    '''
    Reads the values (separated by newlines) and returns them as a list
    of float-values. If None is passed, the function returns an empty list.
    '''
    # Return empty list if None is passed as filename
    if filename is None:
        return []

    # Open the file, read the content and store every line in a list
    # Every line has to contain one measurement value
    values = open(filename, 'r').read().splitlines()

    # Values are read as strings; cast them to floats for plotting
    values = [float(s) for s in values]

    return values


def main():
    '''
    This is the main function that first parses the passed arguments
    (the files containing the values) and then saves the result as a file
    '''
    # Initialize argument parser
    parser = argparse.ArgumentParser()

    # Add argument for reading the measurement results of the FTP message
    # exchange
    parser.add_argument(
        "--ftp_measurement",
        help="Path to the file containing the measurement values for the FTP" +
        " message exchange. If no file is specified, this protocol will be" +
        " ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)

    # Add argument for reading the measurement results of the HTTP message
    # exchange
    parser.add_argument(
        "--http_measurement",
        help="Path to the file containing the measurement values for the HTTP" +
        " message exchange. If no file is specified, this protocol will be" +
        " ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)

    # Add argument for reading the measurement results of the SSH message
    # exchange
    parser.add_argument(
        "--ssh_measurement",
        help="Path to the file containing the measurement values for the SSH" +
        " message exchange. If no file is specified, this protocol will be" +
        " ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)

    # Add argument for the file the plot should be stored in
    parser.add_argument(
        "--output_filename",
        help="Writes the plot to the file specified. The format has to be" +
        " determined by appending the corresponding extension to the filename." +
        " If no filename was specified, then no file will be written." +
        " Existing files will be overwritten. " +
        " Supported formats (any other will lead to an error!):" +
        " eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff",
        type=str,
        default=None)

    # Choice whether to show the plot
    parser.add_argument(
        "--show_plot",
        help="Shows the plot on the screen.",
        action="store_true")

    args = parser.parse_args()

    # Read values from file and store them in a list
    # Do that for all three protocols (FTP, HTTP, SSH)
    ftp_measurement_values = read_values_from_file(
        args.ftp_measurement)
    http_measurement_values = read_values_from_file(
        args.http_measurement)
    ssh_measurement_values = read_values_from_file(
        args.ssh_measurement)

    # Create and store the figure containing the box-plot
    fig = create_boxplot_figure(
        ftp_measurement_values,
        http_measurement_values,
        ssh_measurement_values)

    # If the output filename is not None, save the plot to file
    if args.output_filename is not None:
        save_plot_to_file(fig, args.output_filename)

    # If show_plot is true, show the plot on the screen
    if args.show_plot:
        pyplot.show()

if __name__ == '__main__':
    main()
