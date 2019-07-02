import numpy as np
from matplotlib import pyplot as plt
from shapely import geometry
from scipy import signal
import gdspy
import importlib

# ---------------------------------------------- #
# Grating parameters (change these)
# ---------------------------------------------- #

F = [40e-3, 90e-3, 150e-3] # Feature sizes to iterate over
NP = 6.5 # Number of grating periods
dx = 1e-3 # Step size in x dimension (in microns)
P = 0.300 # Period of grating (in microns)
a = 0.05 # Alligator pitch (in microns)
gds_filename_prefix = "BG" # Name prepended to each gds file
w = 0.5 # waveguide width (in microns)

# ---------------------------------------------- #
# Grating computation (leave these)
# ---------------------------------------------- #

# Some precalculations
N = 1.0/dx # Number of points in x direction
x = np.linspace(0,P*NP-dx,int(N))

# Generate ideal grating polygon
y = a/2*(signal.square(2 * np.pi * (x-P/2)/P,duty=0.5) + 1) + w/2
p = np.array(list(zip(x,y)) + list(zip(x,-y))[::-1])
poly = geometry.Polygon(p)

# Plot ideal case
plt.figure(dpi=100)
plt.plot(*poly.exterior.xy,linewidth = 2, label='Ideal')
# Save ideal case to a GDS file
poly_gds = gdspy.Polygon(p)
ideal_cell = gdspy.Cell('ideal')
ideal_cell.add(poly_gds)
gdspy.write_gds('{}_ideal.gds'.format(gds_filename_prefix))

# Iterate over feature sizes
for curr_F in range(len(F)):
    poly_filt = poly.buffer(-F[curr_F], join_style=1).buffer(F[curr_F], join_style=1)
    poly_filt = poly_filt.buffer(F[curr_F], join_style=1).buffer(-F[curr_F], join_style=1)
    plt.plot(*poly_filt.exterior.xy,'-.',label='Min Feature: {} nm'.format(F[curr_F]*1e3))

    # save new gds file
    importlib.reload(gdspy) # reset the gdspy library
    verts = list(map(list, zip(*poly_filt.exterior.coords.xy)))
    poly_gds = gdspy.Polygon(verts)
    cell = gdspy.Cell('mf={}nm'.format(F[curr_F]*1e3))
    cell.add(poly_gds)
    gdspy.write_gds('{}_mf={}nm.gds'.format(gds_filename_prefix,F[curr_F]*1e3))

# Format plot
plt.legend()
plt.xlabel('x ($\mu$m)')
plt.ylabel('y ($\mu$m)')
plt.grid(True)
plt.tight_layout()
plt.savefig('feature_sizes.png')
plt.show()

