# Silicon Photonic Lithography Simulations
Silicon photonic lithographic platforms are often associated with a particular CMOS node size, which imply a certain minimum feature size. Not only does this dictate the smallest possible resolution between devices (and the devices themselves), but also determines the minimum radius of curvature. In reality, this phenomenon is much more complicated. This explanation, however, serves as a safe approximation for most applications.

This package attempts to simulate the effective geometry as a result of the node constraint for integrated Bragg Gratings. The user can specify a minimum feature size, and the routine will return two GDS files: one for the ideal geometry, and one for the node's specifications.

## Usage
1. Clone the files to your local drive:
```
git clone https://github.com/smartalecH/sim-lithography.git
```

2. Install the requirements into your python environment using pip:
```
pip install -r requirements.txt
```

3. Modify `sim-lithography.py` to include the desired grating parameters and minimum feature size.

4. Run `sim-lithography.py`:
```
python3 sim-lithography.py
```