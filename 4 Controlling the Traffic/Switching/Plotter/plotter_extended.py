'''
Created on 18.01.2015
ACN Project
Plotter

@author: Group 19
'''
import argparse
from matplotlib import pyplot


def create_boxplot_figure(measurements):
    '''
    Reads the input dictionary and plots the results.
    If None is passed, nothing will be plotted.
    Returns a figure containing the box-plot.
    '''
    
    if measurements is None:
        print "Error: Measurements is none!"
        return
    
    # List of value-lists for the three protocols
    values_to_plot = []

    # List of protocol labels
    labels = []

    # Check for all three lists
    # Append the list of results from one protocol to the list of value-lists
    if measurements.has_key("ftp_low"):
        values_to_plot.append(measurements["ftp_low"])
        labels.append("FTP (low)")
    if measurements.has_key("ftp_med"):
        values_to_plot.append(measurements["ftp_med"])
        labels.append("FTP (medium)")
    if measurements.has_key("ftp_high"):
        values_to_plot.append(measurements["ftp_high"])
        labels.append("FTP (high)")
    if measurements.has_key("http_low"):
        values_to_plot.append(measurements["http_low"])
        labels.append("HTTP (low)")
    if measurements.has_key("http_med"):
        values_to_plot.append(measurements["http_med"])
        labels.append("HTTP (medium)")
    if measurements.has_key("http_high"):
        values_to_plot.append(measurements["http_high"])
        labels.append("HTTP (high)")
    if measurements.has_key("ssh_low"):
        values_to_plot.append(measurements["ssh_low"])
        labels.append("SSH (low)")
    if measurements.has_key("ssh_med"):
        values_to_plot.append(measurements["ssh_med"])
        labels.append("SSH (medium)")
    if measurements.has_key("ssh_high"):
        values_to_plot.append(measurements["ssh_high"])
        labels.append("SSH (high)")

    # Create one plot-figure
    fig = pyplot.figure(1, figsize=(20, 10))

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
    # exchange at low bandwidth
    parser.add_argument(
        "--ftp_low",
        help="Path to the file containing the measurement values for the FTP" +
        " message exchange at low bandwidth. If no file is specified, this protocol" +
        " will be ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)
    # Add argument for reading the measurement results of the FTP message
    # exchange at low bandwidth
    parser.add_argument(
        "--ftp_med",
        help="Path to the file containing the measurement values for the FTP" +
        " message exchange at medium bandwidth. If no file is specified, this protocol" +
        " will be ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)
    # Add argument for reading the measurement results of the FTP message
    # exchange at low bandwidth
    parser.add_argument(
        "--ftp_high",
        help="Path to the file containing the measurement values for the FTP" +
        " message exchange at high bandwidth. If no file is specified, this protocol" +
        " will be ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)
    # Add argument for reading the measurement results of the FTP message
    # exchange at low bandwidth
    parser.add_argument(
        "--http_low",
        help="Path to the file containing the measurement values for the HTTP" +
        " message exchange at low bandwidth. If no file is specified, this protocol" +
        " will be ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)
    # Add argument for reading the measurement results of the FTP message
    # exchange at low bandwidth
    parser.add_argument(
        "--http_med",
        help="Path to the file containing the measurement values for the HTTP" +
        " message exchange at medium bandwidth. If no file is specified, this protocol" +
        " will be ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)
    # Add argument for reading the measurement results of the FTP message
    # exchange at low bandwidth
    parser.add_argument(
        "--http_high",
        help="Path to the file containing the measurement values for the HTTP" +
        " message exchange at high bandwidth. If no file is specified, this protocol" +
        " will be ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)
    # Add argument for reading the measurement results of the FTP message
    # exchange at low bandwidth
    parser.add_argument(
        "--ssh_low",
        help="Path to the file containing the measurement values for the SSH" +
        " message exchange at low bandwidth. If no file is specified, this protocol" +
        " will be ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)
    # Add argument for reading the measurement results of the FTP message
    # exchange at low bandwidth
    parser.add_argument(
        "--ssh_med",
        help="Path to the file containing the measurement values for the SSH" +
        " message exchange at medium bandwidth. If no file is specified, this protocol" +
        " will be ignored. The values are floating point values and have to be" +
        " separated by line-breaks.",
        type=str,
        default=None)
    # Add argument for reading the measurement results of the FTP message
    # exchange at low bandwidth
    parser.add_argument(
        "--ssh_high",
        help="Path to the file containing the measurement values for the SSH" +
        " message exchange at high bandwidth. If no file is specified, this protocol" +
        " will be ignored. The values are floating point values and have to be" +
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

    # Create dictionary that contains the measurements
    measurements = {}

    # Read values from files and store them in a dictionary
    # Do that for all three protocols (FTP, HTTP, SSH)
    # and all three bandwidths (if available)
    if args.ftp_low is not None:
        measurements["ftp_low"] = read_values_from_file(args.ftp_low)
    if args.ftp_med is not None:
        measurements["ftp_med"] = read_values_from_file(args.ftp_med)
    if args.ftp_high is not None:
        measurements["ftp_high"] = read_values_from_file(args.ftp_high)
    if args.http_low is not None:
        measurements["http_low"] = read_values_from_file(args.http_low)
    if args.http_med is not None:
        measurements["http_med"] = read_values_from_file(args.http_med)
    if args.http_high is not None:
        measurements["http_high"] = read_values_from_file(args.http_high)
    if args.ssh_low is not None:
        measurements["ssh_low"] = read_values_from_file(args.ssh_low)
    if args.ssh_med is not None:
        measurements["ssh_med"] = read_values_from_file(args.ssh_med)
    if args.ssh_high is not None:
        measurements["ssh_high"] = read_values_from_file(args.ssh_high)

    # Create and store the figure containing the box-plot
    fig = create_boxplot_figure(measurements)

    # If the output filename is not None, save the plot to file
    if args.output_filename is not None:
        save_plot_to_file(fig, args.output_filename)

    # If show_plot is true, show the plot on the screen
    if args.show_plot:
        pyplot.show()

if __name__ == '__main__':
    main()
