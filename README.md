# Silicon Photonic Lithography Simulations
Silicon photonic lithographic platforms are often associated with a particular CMOS node size, which imply a certain minimum feature size. Not only does this dictate the smallest possible resolution between devices (and the devices themselves), but also determines the minimum radius of curvature. In reality, this phenomenon is much more complicated. This explanation, however, serves as a safe approximation for most applications.



## Basic Setup
1. Clone the files to your local drive:
```
git clone https://github.com/smartalecH/sim-lithography.git
```

2. Install the requirements into your python environment using pip:
```
pip install -r requirements.txt
```

## Transform Existing GDS Files

You can use the `transform_GDS.py` script to transform an existing GDS file such that all of the embedded geometries are rounded to be consistent with a particular node size. Simply run the script and pass the GDS filename and desired node size (in nm) as command line arguments. For example, we can transform the `BG_ideal.gds` file using a 45 nm node size with
```
python3 transform_GDS.py BG_ideal.gds 45
```

We can then look at the newly created `BG_ideal_45nm.gds` file.

## Bragg Grating Example

Rather than converting existing GDS files, you can script your geometry in python (using your favorite geometry package) and run the same few lines of code to round the hard corners of your geometry consistent with a particular node size. For example, we can write a script that designs and rounds integrated Bragg Gratings. The user can specify a minimum feature size, and the routine will return two GDS files: one for the ideal geometry, and one for the node's specifications.

1. Modify `sim_BG.py` to include the desired grating parameters and minimum feature size(s).

2. Run `sim_BG.py`:
```
python3 sim_BG.py
```