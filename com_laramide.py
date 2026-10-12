#!/usr/bin/env python
import sys
import numpy
import os
import errno
output_name = "com_laramide"
output_dir = r"C:\Users\Lenovo\Desktop\homework\finalessay\second\python_output"
xmin = 0.0
xmax = 6000.0e3
ymin = 0.0
ymax = 800.0e3
xnum = 1200
ynum = 160
x_gap = 500.0e3
x_SP  = 3000.0e3
OP_Keel_Start_PTx = x_gap + x_SP + 800.0e3
y_crust = 7.5e3
radius_outer = 245.0e3
depth_notch = 200.0e3
slab_dip = 70.0
OPthick = 120.0e3
OP_Keel_Thick = OPthick / 2.0
No_nodes = (xnum + 1) * (ynum + 1)
C = numpy.zeros([No_nodes, 7], float)
ind = 0
print("writing text file...")
for j in range(ynum + 1):
    for i in range(xnum + 1):
        x = xmin + i * ((xmax - xmin) / xnum)
        y = ymin + j * ((ymax - ymin) / ynum)
        C[ind, 0] = x
        C[ind, 1] = y
        C[ind, 5] = 0.0
        C[ind, 6] = 0.0
        if x > x_gap and x <= x_gap + x_SP - radius_outer and y > ymax - y_crust:
            C[ind, 2] = 1.0
        elif x > x_gap + x_SP - radius_outer and x < x_gap + x_SP:
            x1 = x_gap + x_SP - radius_outer
            y1 = ymax - radius_outer
            if ((x - x1)**2 + (y - y1)**2) < radius_outer**2 and \
               ((x - x1)**2 + (y - y1)**2) >= (radius_outer - y_crust)**2 and \
               y > ymax - depth_notch:
                angle = numpy.arctan((y - y1) / (x - x1))
                if angle > numpy.radians(90.0 - slab_dip):
                    C[ind, 2] = 1.0
        if x > x_gap + x_SP - radius_outer and x < x_gap + x_SP:
            x1 = x_gap + x_SP - radius_outer
            y1 = ymax - radius_outer
            if ((x - x1)**2 + (y - y1)**2) >= radius_outer**2 and y > ymax - OPthick:
                C[ind, 3] = 1.0
        if x > OP_Keel_Start_PTx and x < xmax - x_gap and \
           y <= ymax - OP_Keel_Thick and y >= ymax - OPthick:
            C[ind, 4] = 1.0
        else:
            if x >= x_gap + x_SP and x < xmax - x_gap and y >= ymax - OPthick:
                C[ind, 3] = 1.0
        ind += 1
if not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
text_file_name = os.path.join(output_dir, output_name + '.txt')
with open(text_file_name, "w+") as f:
    f.write("# POINTS: %s %s\n" % (str(xnum + 1), str(ynum + 1)))
    f.write("# Columns: x y composition1 composition2 composition3\n")
    for k in range(ind):
        f.write("%.6f %.6f %.6f %.6f %.6f\n" % (C[k, 0], C[k, 1], C[k, 2], C[k, 3], C[k, 4]))
print("file written:", text_file_name)