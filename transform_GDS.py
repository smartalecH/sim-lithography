import numpy as np
from matplotlib import pyplot as plt
from shapely import geometry
from scipy import signal
import gdspy
import importlib
import argparse

# ---------------------------------------------- #
# Parse the input arguments
# ---------------------------------------------- #

parser = argparse.ArgumentParser(description='Simulate the effects of lithography for a particular node size on a GDS file.')
parser.add_argument('filename', type=str, help='filename of input GDS')
parser.add_argument('node_size', type=float, help='Node size in nanometers')
args = parser.parse_args()

# ---------------------------------------------- #
# Read in the GDS file
# ---------------------------------------------- #

input_filename = args.filename
node_size = args.node_size

output_filename = '{}_{}nm.gds'.format(input_filename[:-4],int(node_size))

gdsii = gdspy.GdsLibrary(infile=input_filename)

polygons = []
top_cells = gdsii.top_level()
for ci, c in enumerate(top_cells):
    polygons.append(c.get_polygons())

# ---------------------------------------------- #
# Process the polygons
# ---------------------------------------------- #
node_size_um = node_size * 1e-3

importlib.reload(gdspy) # reset the gdspy library
# Iterate through polygons
for pi, p in enumerate(polygons):
    poly = geometry.Polygon(np.squeeze(p))
    poly_filt = poly.buffer(-node_size_um, join_style=1).buffer(node_size_um, join_style=1)
    poly_filt = poly_filt.buffer(node_size_um, join_style=1).buffer(-node_size_um, join_style=1)
    verts = list(map(list, zip(*poly_filt.exterior.coords.xy)))
    poly_gds = gdspy.Polygon(verts)
    cell = gdspy.Cell('p={}'.format(pi))
    cell.add(poly_gds)


# ---------------------------------------------- #
# Save the new GDS file
# ---------------------------------------------- #

gdspy.write_gds(output_filename)

quit()

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