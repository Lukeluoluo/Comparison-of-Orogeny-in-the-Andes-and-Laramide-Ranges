#!/usr/bin/env python
import sys
import os
import errno
import numpy as np
import scipy.special
output_name = "tem_laramide"
output_dir = r"C:\Users\Lenovo\Desktop\homework\finalessay\second\python_output"
xmin = 0.0
xmax = 6000.0e3
ymin = 0.0
ymax = 800.0e3
xnum = 1200
ynum = 160
x_gap = 500.0e3
x_SP  = 3000.0e3
depth_notch  = 200.0e3
radius_outer = 245.0e3
slab_dip = 70.0
ridge_extent = 0.0e3
OPthick = 120.0e3
Tmax = 1273.0
Tmin = 273.0
Tcutoff = 1273.0
age_ma = 100
age = age_ma * 1e6 * 365 * 24 * 60 * 60
age_op_ma = 130
age_op = age_op_ma * 1e6 * 365 * 24 * 60 * 60
k = 1e-6
No_nodes = (xnum + 1) * (ynum + 1)
T = np.zeros([No_nodes, 3], float)
ind = 0
print("writing text file...")
for j in range(ynum + 1):
    for i in range(xnum + 1):
        x = xmin + i * ((xmax - xmin) / xnum)
        y = ymin + j * ((ymax - ymin) / ynum)
        T[ind, 0] = x
        T[ind, 1] = y
        T[ind, 2] = Tmax
        if x > x_gap and x <= x_gap + x_SP - radius_outer:
            erf_term = (ymax - y) / (2 * np.sqrt(k * age))
            T[ind, 2] = Tmax - (Tmax - Tmin) * scipy.special.erfc(erf_term)
        elif x >= x_gap + x_SP and x < xmax - x_gap:
            erf_term = (ymax - y) / (2 * np.sqrt(k * age_op))
            T[ind, 2] = Tmax - (Tmax - Tmin) * scipy.special.erfc(erf_term)
        if x > x_gap + x_SP - radius_outer and x < x_gap + x_SP:
            x1 = x_gap + x_SP - radius_outer
            y1 = ymax - radius_outer
            if ((x - x1)**2 + (y - y1)**2) < radius_outer**2 and y > ymax - depth_notch:
                angle = np.arctan((y - y1) / (x - x1))
                if angle > np.radians(90.0 - slab_dip):
                    ynotch = radius_outer - np.sqrt((x - x1)**2 + (y - y1)**2)
                    erf_term = ynotch / (2 * np.sqrt(k * age))
                    T[ind, 2] = Tmax - (Tmax - Tmin) * scipy.special.erfc(erf_term)
            elif ((x - x1)**2 + (y - y1)**2) >= radius_outer**2 and y > ymax - depth_notch:
                erf_term = (ymax - y) / (2 * np.sqrt(k * age_op))
                T[ind, 2] = Tmax - (Tmax - Tmin) * scipy.special.erfc(erf_term)
        if T[ind, 2] > Tcutoff:
            T[ind, 2] = Tmax
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
    f.write("# Columns: x y temperature\n")
    for k in range(ind):
        f.write("%.6f %.6f %.6f\n" % (T[k, 0], T[k, 1], T[k, 2]))
print("file written:", text_file_name)