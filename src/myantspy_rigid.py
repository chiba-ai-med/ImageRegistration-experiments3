# -*- coding: utf-8 -*-
import sys
import ants
import numpy as np
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.functions import csv2img3
import pickle

# Arguments
args = sys.argv
infile1 = args[1]
infile2 = args[2]
infile3 = args[3]
infile4 = args[4]
infile5 = args[5]
infile6 = args[6]
outfile1 = args[7]
outfile2 = args[8]
outfile3 = args[9]
outfile4 = args[10]

# Loading
source_exp = np.loadtxt(infile1)
target_exp = np.loadtxt(infile2)
source_x_corrdinate = np.loadtxt(infile3, dtype='int')
target_x_corrdinate = np.loadtxt(infile4, dtype='int')
source_y_corrdinate = np.loadtxt(infile5, dtype='int')
target_y_corrdinate = np.loadtxt(infile6, dtype='int')

# Numpy => ANTs Object
moving_image = ants.from_numpy(csv2img3(source_x_corrdinate, source_y_corrdinate, source_exp))
fixed_image = ants.from_numpy(csv2img3(target_x_corrdinate, target_y_corrdinate, target_exp))

# Image Registration
mytx = ants.registration(fixed=fixed_image, moving=moving_image, type_of_transform='Rigid')

# Warping
warped = mytx['warpedmovout']
warped_np = warped.numpy()
warped_np_vec = warped_np.T.flatten()

# Save
np.savetxt(outfile1, warped_np)
np.savetxt(outfile2, warped_np_vec)

with open(outfile3, 'wb') as f:
    pickle.dump(warped, f)

with open(outfile4, 'wb') as f:
    pickle.dump(mytx, f)
