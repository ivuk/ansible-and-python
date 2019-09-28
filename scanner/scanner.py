#!/usr/bin/env python3

import nmap
import sys
import os
import glob
import filecmp
import shutil

# GNU/Linux specific
FILE_PATH = "/dev/shm"

# FIXME: There's tons of better ways for handling arguments
# Make sure we have only one argument passed to the script
if len(sys.argv) != 2:
    print(
        "This script accepts exactly one argument.\n"
        "Example usage:\n"
        "./scanner.py 127.0.0.1\n"
        "./scanner.py 127.0.0.1/8"
    )
    exit(14)

# The first argument should be either the host or the subnet
scanhost = sys.argv[1]

# Get nmap to do the scanning for us
nm = nmap.PortScanner()
nm.scan(scanhost)

# Run through each specified host
for host in nm.all_hosts():
    # Check if we have a file from the prior run for this host
    # Set the file name depending on the results of the check
    FILE_PATTERN = "{}/python-scanner-{}-*".format(FILE_PATH, host)
    FILE_NAME = "{}/python-scanner-{}-1".format(FILE_PATH, host)
    previous_scan = False

    for obj in glob.glob(FILE_PATTERN):
        if os.path.isfile(obj):
            FILE_NAME = "{}/python-scanner-{}-2".format(FILE_PATH, host)
            ORIG_FILE_NAME = "{}/python-scanner-{}-1".format(FILE_PATH, host)
            previous_scan = True

    # Write out the file first
    with open(FILE_NAME, "w") as f:
        f.write("*Target - {}: Full scan results:*\n".format(host))

        for protocol in nm[host].all_protocols():
            ports = nm[host][protocol].keys()

            for port in ports:
                f.write(
                    "Host: {}\tPorts: {}/{}/{}////\n".format(
                        host, port, nm[host][protocol][port]["state"], protocol
                    )
                )

    # Compare the results from the two runs
    # If they're the same, print the placeholder text
    # Otherwise print the scan results
    if previous_scan:
        if filecmp.cmp(FILE_NAME, ORIG_FILE_NAME):
            print("*Target - {}: No new records found in the last scan.*".format(host))

            # Replace the old file with the new scan data
            shutil.copy2(FILE_NAME, ORIG_FILE_NAME)
            # Remove the file with the data from the current run
            os.remove(FILE_NAME)

    else:
        # FIXME: Don't do the same work twice
        # Write the results to stdout
        print("*Target - {}: Full scan results:*".format(host))
        for protocol in nm[host].all_protocols():
            ports = nm[host][protocol].keys()

            for port in ports:
                print(
                    "Host: {}\tPorts: {}/{}/{}////".format(
                        host, port, nm[host][protocol][port]["state"], protocol
                    )
                )
