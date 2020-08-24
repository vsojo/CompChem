#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
<gmx_log_processor.py>
Takes a GROMACS mdrun .log file and makes a CSV file of energy
values ready for analysis or plotting in e.g. Microsoft Excel,
R, MatPlotLib and the like.

This script was developed in August 2020 when the Xmgrace website
was not working for downloading the software. The script is provided
"as is" and we take absolutely no responsibility for anything that
goes wrong, e.g. if it gives you incorrect results, deletes your data,
or whatever (it shouldn't do any of those things, though!).

We STRONGLY recommend checking at least a few values in your input
.log file to make sure they match those in the output CSV file.

EXAMPLE:
    python3 gmx_log_processor.py -i my_md.log -o my_md.csv

    ... where -i is for input, -o for output

RUNNING AND INSTALLATION:
    You can remove the 'python3' and turn this script into recognisable software that you can run 
    from anywhere in your system by doing the following:
     1. Make the script executable by executing the following in the shell:
            chmod 755 gmx_log_processor.py
     2. Put it in a place where your shell can find it, e.g. you could make a directory called 'bin'
        and put your executable scripts there, then add that directory to your $PATH variable. So,
        at your own risk and discretion, you could add this line to your .bash_profile, .bashrc, .zshrc,
        or whichever approriate file controls your shell sessions:
            PATH=$PATH:/Users/MyUserName/MySoftware/bin
        Where that directory is whichever directory you want to put this script in.
     3. Edit the first line of this script to make sure it points to wherever your python3 is. You can
        normally find out by running:
            which python3
        If your system can't find python3, you probably don't have it installed, but hopefully you'll
        see something like:
            /Users/MyUserName/opt/anaconda3/bin/python3
        OK, now the script should be findable and executable.
     4. Optional: you could remove the .py from the name, so that it looks more like a command. Go to
        wherever you put the script and change its name:
            mv gmx_log_processor.py gmx_log_processor

        Now you should be able to run it from anywhere like this:
            gmx_log_processor -f my_md.log -o my_md.csv

Version: 0.01
Author: Victor Sojo, vsojo@amnh.org / v.sojo@lmu.de
"""

import argparse
from collections import defaultdict

# Create the argument parser, and give it a description for the script's help:
parser = argparse.ArgumentParser(
    description = """
   ### Example run:  python3 gmx_log_processor.py -i my_md.log -o my_md.csv  ###

    ... where -i is for input, -o for output.

This script <gmx_log_processor.py> takes a GROMACS mdrun .log file 
and makes a CSV file of energy values ready for analysis or plotting
in e.g. Microsoft Excel, R, MatPlotLib and the like.

This script was developed in August 2020 when the Xmgrace website
was not working for downloading the software (which is meant to plot
energy output from GROMACS MD simulations). The script is provided
"as is" and we take absolutely no responsibility for anything that
goes wrong, e.g. if it gives you incorrect results, deletes your data,
or whatever (it shouldn't do any of those things, though!).

We STRONGLY recommend checking at least a few values in your input
.log file to make sure they match those in the output CSV file.

Please open the script file itself for further information.
Version: 0.01
Author: Victor Sojo, vsojo@amnh.org / v.sojo@lmu.de
"""
)

parser.add_argument('-i', '--infile'
                    , dest = 'infile'
                    , help = "This is a GROMACS .log file with energies, created by mdrun (e.g. <em.log>)."
                    , required = True
)
parser.add_argument('-o', '--outfile'
                    , dest = 'outfile'
                    , help = "Name of a .csv file to write as output (will replace if already exists!)."
                    , required = True
)

# Execute the parser to read any arguments given to the script on the command line:
args = parser.parse_args()
# Read the relevant arguments
infile  = args.infile
outfile = args.outfile

energies = defaultdict(list)
gromacs_steps = None

with open(infile) as f:
    for line in f:
        line = line.strip()
        if line.split() == ['Step', 'Time']:
            # Extract the step and time from the next line
            step, time = next(f).strip().split()
        elif "converged to Fmax <" in line and "steps" in line:
            gromacs_steps = line.split()[-2]
        elif line == "Energies (kJ/mol)":
            # Initialise the step and time to the last values found
            field_names = ['step', 'time']
            field_vals  = [step, time]

            # GET THE FIRST LINE WITH ENERGY NAMES
            line = next(f).strip()
            while line:
                # Fix the names have spaces in the wrong places
                line = line.replace("Proper Dih.", "Proper_Dih.")
                line = line.replace(" (SR)", "_(SR)")
                line = line.replace("Coul. recip.", "Coul._recip.")
                line = line.replace("Pressure (bar)", "Pressure_(bar)")
                #line = line.replace('.', '')

                # Split the line to get the names
                field_names.extend(line.split())
                
                # GET THE FOLLOWING LINE, WHICH SHOULD HAVE THE CORRESPONDING VALUES   
                line = next(f)
                field_vals.extend(line.split())
                
                # Read the following line, which may contain further fields, or be empty
                # (if it's empty) we'll just exit the while loop and wait for the next block
                line = next(f)
                line = line.strip()
            
            # Convert all values to floats
            #field_vals = [float(val) for val in field_vals]

            for field, val in zip(field_names, field_vals):
                energies[field].append(val)
            # end for: 
        # end if: is this the beginning of an Energy block?
    # end for: reading the file line by line
# end with: processing the input file

# How many proper entries did we have?
n_entries = len(energies['step'])
# # # # #  WARNING !!!!  # # # # #
# Apparently, GROMACS runs some steps without printing data
# So the number of steps is not the same as the number of entries.
# Check your .log file!

# Create the output CSV file 
with open(outfile, 'w') as f:
    # HEADER
    # Add all of the energy types that we have stored above
    # If you want to keep the _ instead of space, just change the second ' ' to '_'
    # to do a replace from _ to _ (i.e. leaving it unchanged)
    f.write(','.join([key.replace('_',' ') for key in energies.keys()]) + '\n')
    
    # VALUES
    # Now go over each set of results and print them line by line to the CSV file
    for i in range(n_entries):
        f.write(','.join( [energies[field][i] for field in energies.keys()] ) + '\n')
    # end for: printing results of each step line by line to the CSV file
# end with: done working with the output CSV file

nhashes = 34
print("\n\n" + nhashes*"# ")
print("#" + (nhashes-2)*"  " + " #\n")
print(f"FINISHED PROCESSING GROMACS LOG FILE <{infile}>\n")
print(f"The total number of steps according to GROMACS was {gromacs_steps}.")
print(f"Starting at {energies['step'][0]}, the last step in the log file is marked as {energies['step'][-1]}.")
print(f"Of these, {n_entries} had energy data, so output file <{outfile}>")
print(f"has {n_entries} data points for the different energetic variables.")
print(f"The remaining steps had no energy data that could be parsed.\n")
print(f"PLEASE EXAMINE YOUR .LOG FILE AND COMPARE IT WITH THE .CSV FILE!!!\n")
print("#" + (nhashes-2)*"  " + " #")
print(34*"# " + "\n\n")
