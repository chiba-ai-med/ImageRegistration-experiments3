# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import pandas as pd
import pickle

# Arguments
args = sys.argv
infile_source_exp = args[1]   # data/{dataset}/source/all_exp.csv
infile_target_exp = args[2]   # data/{dataset}/target/all_exp.csv
infile_source_x = args[3]     # data/{dataset}/source/x.csv
infile_target_x = args[4]     # data/{dataset}/target/x.csv
infile_source_y = args[5]     # data/{dataset}/source/y.csv
infile_target_y = args[6]     # data/{dataset}/target/y.csv
outfile_warped = args[7]      # output/{dataset}/ir_*/warped.txt
outfile_tx = args[8]          # output/{dataset}/ir_*/tx.pkl
ref_type = args[9]            # "sum_exp" or "anatomy"
transform_type = args[10]     # "rigid", "affine", "sitk_rigid"
# Optional: anatomy files for ref_type="anatomy"
infile_source_anat = args[11] if len(args) > 11 else None
infile_target_anat = args[12] if len(args) > 12 else None

def csv2img(x, y, exp):
    img = np.zeros((x.max() - x.min() + 1, y.max() - y.min() + 1))
    img[x - x.min(), y - y.min()] = exp
    return img

# Loading
source_all_exp = pd.read_csv(infile_source_exp, header=0)
target_all_exp = pd.read_csv(infile_target_exp, header=0)
source_x = np.loadtxt(infile_source_x, dtype=int)
target_x = np.loadtxt(infile_target_x, dtype=int)
source_y = np.loadtxt(infile_source_y, dtype=int)
target_y = np.loadtxt(infile_target_y, dtype=int)

source_cols = source_all_exp.columns.to_numpy()
n_target = len(target_x)
n_features = source_all_exp.shape[1]

print(f"Source: {source_all_exp.shape}, Target: {target_all_exp.shape}")
print(f"Source grid: ({source_x.max()-source_x.min()+1})x({source_y.max()-source_y.min()+1})")
print(f"Target grid: ({target_x.max()-target_x.min()+1})x({target_y.max()-target_y.min()+1})")
print(f"Reference: {ref_type}, Transform: {transform_type}")

# Create reference images for registration
if ref_type == "sum_exp":
    source_ref = source_all_exp.values.sum(axis=1)
    target_ref = target_all_exp.values.sum(axis=1)
elif ref_type == "anatomy":
    source_anat = pd.read_csv(infile_source_anat, header=0)
    target_anat = pd.read_csv(infile_target_anat, header=0)
    # Convert one-hot to integer labels (argmax + 1 to avoid 0=background)
    source_ref = source_anat.values.argmax(axis=1).astype(float) + 1
    target_ref = target_anat.values.argmax(axis=1).astype(float) + 1
else:
    raise ValueError(f"Unknown ref_type: {ref_type}")

moving_img = csv2img(source_x, source_y, source_ref)
fixed_img = csv2img(target_x, target_y, target_ref)

print(f"Moving image: {moving_img.shape}, Fixed image: {fixed_img.shape}")

# Register
if transform_type in ["rigid", "affine"]:
    import ants
    moving = ants.from_numpy(moving_img.astype(np.float64))
    fixed = ants.from_numpy(fixed_img.astype(np.float64))
    tx_type = 'Rigid' if transform_type == "rigid" else 'Affine'
    print(f"Running ANTsPy {tx_type} registration...")
    mytx = ants.registration(fixed=fixed, moving=moving, type_of_transform=tx_type)
    fwd_transforms = mytx['fwdtransforms']

    # Warp each source feature and sample at target locations
    warped_features = np.zeros((n_target, n_features))
    target_x_idx = target_x - target_x.min()
    target_y_idx = target_y - target_y.min()

    for i in range(n_features):
        feat_img = csv2img(source_x, source_y, source_all_exp.iloc[:, i].values)
        feat_ants = ants.from_numpy(feat_img.astype(np.float64))
        warped_feat = ants.apply_transforms(fixed=fixed, moving=feat_ants,
                                            transformlist=fwd_transforms)
        warped_np = warped_feat.numpy()
        warped_features[:, i] = warped_np[target_x_idx, target_y_idx]

    tx_save = mytx

elif transform_type == "sitk_rigid":
    import SimpleITK as sitk
    moving = sitk.GetImageFromArray(moving_img.astype(np.float64))
    fixed = sitk.GetImageFromArray(fixed_img.astype(np.float64))

    print("Running SimpleITK Rigid registration...")
    rigid_transform = sitk.CenteredTransformInitializer(
        fixed, moving, sitk.Euler2DTransform(),
        sitk.CenteredTransformInitializerFilter.GEOMETRY)

    reg = sitk.ImageRegistrationMethod()
    reg.SetMetricAsMeanSquares()
    reg.SetOptimizerAsRegularStepGradientDescent(
        learningRate=1.0, minStep=1e-4, numberOfIterations=200)
    reg.SetOptimizerScalesFromPhysicalShift()
    reg.SetInitialTransform(rigid_transform, inPlace=False)
    reg.SetInterpolator(sitk.sitkLinear)
    mytx = reg.Execute(fixed, moving)

    # Warp each source feature
    warped_features = np.zeros((n_target, n_features))
    target_x_idx = target_x - target_x.min()
    target_y_idx = target_y - target_y.min()

    for i in range(n_features):
        feat_img = csv2img(source_x, source_y, source_all_exp.iloc[:, i].values)
        feat_sitk = sitk.GetImageFromArray(feat_img.astype(np.float64))
        warped_feat = sitk.Resample(feat_sitk, fixed, mytx, sitk.sitkLinear,
                                     0.0, feat_sitk.GetPixelID())
        warped_np = sitk.GetArrayFromImage(warped_feat)
        warped_features[:, i] = warped_np[target_x_idx, target_y_idx]

    tx_save = mytx

else:
    raise ValueError(f"Unknown transform_type: {transform_type}")

# Save
os.makedirs(os.path.dirname(outfile_warped), exist_ok=True)
out = pd.DataFrame(warped_features, columns=source_cols)
out.to_csv(outfile_warped, index=False)

with open(outfile_tx, 'wb') as f:
    pickle.dump(tx_save, f)

print("Done.")
