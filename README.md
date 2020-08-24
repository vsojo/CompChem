# Computational Chemistry scripts
This repository is meant to contain (hopefully) helpful script for computational-chemistry work.
## Contents
* [`gmx_log_processor.py`: a script to process to extract energy values from GROMACS `mdrun` output for plotting.](#gmx_log_processor.py)

# Scripts
## <a name='gmx_log_processor.py'></a> `gmx_log_processor.py`
Takes a `.log` file from a GROMACS `mdrun` simulation and makes a comma-separated-values (`.csv`) file of energy values that can be used for plotting in Microsoft Excel,R, MatPlotLib and the like.

### Example run
`python3 gmx_log_processor.py -i my_md.log -o my_md.csv`
... where `-i` is for input and `-o` for output

### A simpler (and likely better) alternative to this script
[Justin A. Lemkul](https://www.biochem.vt.edu/people/faculty/JustinLemkul.html) at VirginiaTech suggests that providing the `-xvg none` flag to `gmx energy` is a much easier way of getting this information:
`gmx energy -f my_em.edr -o potential.xvg -xvg none`

### History
This script was developed in August 2020 when the [https://plasma-gate.weizmann.ac.il/Grace/](Xmgrace website) failed for some unknown reason. I developed this script as a replacement, for my own use, to parse the `mdrun` output from GROMACS and give out tables of energy values that can be easily plotted in e.g. Excel. Again: the Grace website was broken, I needed to analyse `mdrun` output, so I wrote this script. Feel free to use it, but please note the warnings at the end!

### Installing for long-term usage
You can remove the 'python3' and turn this script into recognisable software that you can run from anywhere in your system by doing the following:
1. Make the script executable by executing the following in the shell:
`chmod 755 gmx_log_processor.py`

2. Put it in a place where your shell can find it, e.g. you could make a directory called `bin` and put your executable scripts there, then add that directory to your `$PATH` variable. So, _at your own risk and discretion_, you could add this line to your `.bash_profile`, `.bashrc`, `.zshrc`, or whichever approriate file controls your shell sessions:
`PATH=$PATH:/Users/MyUserName/MySoftware/bin`
Where that directory is whichever directory you want to put this script in.

3. Edit the first line of this script to make sure it points to wherever your `python3` is. You can normally find out by running:
`which python3`
If your system can't find python3, you probably don't have it installed, but hopefully you'll see something like:
`/Users/MyUserName/opt/anaconda3/bin/python3`
OK, now the script should be findable and executable.

4. _Optional:_ you could remove the `.py` from the name, so that it looks more like a command. Go to wherever you put the script and change its name:
`mv gmx_log_processor.py gmx_log_processor`
... and now you should be able to run it from anywhere like this:
`gmx_log_processor -f my_md.log -o my_md.csv`


### :warning: Warnings :warning:

:construction: Please consider this script a _under construction_ :construction:

_The script is provided "as is" and I take absolutely no responsibility for anything that goes wrong, e.g. if it gives you incorrect results, deletes your data, or whatever._

It hopefully shouldn't do any of those things, though! And on that note, if you do find a bug, I would be very grateful if you could please point me to it so that I can fix it as soon as possible. Same if you find a way to improve it and want to collaborate.

In any case:

:rotating_light: **I STRONGLY recommend that you check at least a few values in your input `.log` file to make sure they match those in the output of the `.csv` file that the script produces.** :rotating_light:
