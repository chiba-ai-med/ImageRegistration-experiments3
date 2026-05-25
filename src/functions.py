import SimpleITK as sitk
import re
import numpy as np

def renumber_sequence(sequence):
    unique_values = {value: idx for idx, value in enumerate(sorted(set(sequence)))}
    return [unique_values[value] for value in sequence]

def csv2img3(x, y, exp):
    img_array = np.zeros((max(x) - min(x) + 1, max(y) - min(y) + 1))
    img_array[x - min(x), y - min(y)] = exp
    return img_array

def apply_function_to_columns(dataframe, func, **kwargs):
    result_list = [func(dataframe[col], **kwargs) for col in dataframe.columns]
    return result_list

def csv2img_eachcol(exp, x, y):
    return csv2img2(x, y, exp)

def csv2img2(x, y, exp):
    img_array = np.zeros((max(x) - min(x) + 1, max(y) - min(y) + 1))
    img_array[x - min(x), y - min(y)] = exp.to_numpy()
    return img_array

def res_source(infile):
    # SMA
    ## (56, 62) => (1120, 1240)
    if(re.match(".*sma_neg_trs", infile)):
            return 20
    # Public
    ## (38, 50) => (1026, 1350)
    if(re.match(".*public_neg_trs", infile)):
            return 27

def res_target(infile):
    # SMA
    ## (37939, 34861) => (3793, 3486)
    if(re.match(".*sma_neg_trs", infile)):
            # return 0.1
            return 0.333
    # Public
    ## (6606, 8741) => (1056, 1398)
    if(re.match(".*public_neg_trs", infile)):
            # return 0.16
            return 1

def csv2img(x, y, exp):
    img_array = np.zeros((max(x) - min(x) + 1, max(y) - min(y) + 1))
    img_array[x - min(x), y - min(y)] = exp.to_numpy()[:,0]
    return img_array

def resample_image(input, scale):
    # 元の画像のサイズとピクセル間隔を取得
    original_size = input.GetSize()
    original_spacing = input.GetSpacing()

    # 新しいサイズと間隔を計算
    new_size = [int(sz * scale) for sz in original_size]
    new_spacing = [sp / scale for sp in original_spacing]

    # Resampleフィルターを設定
    resampler = sitk.ResampleImageFilter()
    resampler.SetSize(new_size)
    resampler.SetOutputSpacing(new_spacing)
    # 補間方法の設定
    resampler.SetInterpolator(sitk.sitkGaussian)
    # resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    # resampler.SetInterpolator(sitk.sitkLinear)
    # resampler.SetInterpolator(sitk.sitkBSpline)
    resampler.SetOutputOrigin(input.GetOrigin())    
    resampler.SetOutputDirection(input.GetDirection())
    resampler.SetTransform(sitk.Transform())
    resampler.SetDefaultPixelValue(0)

    # 解像度を変更した画像を生成
    return resampler.Execute(input)

def resample_image_categorical(input, scale):
    # 元の画像のサイズとピクセル間隔を取得
    original_size = input.GetSize()
    original_spacing = input.GetSpacing()

    # 新しいサイズと間隔を計算
    new_size = [int(sz * scale) for sz in original_size]
    new_spacing = [sp / scale for sp in original_spacing]

    # Resampleフィルターを設定
    resampler = sitk.ResampleImageFilter()
    resampler.SetSize(new_size)
    resampler.SetOutputSpacing(new_spacing)
    resampler.SetInterpolator(sitk.sitkGaussian)  # Nearest Neighbor補間を使用
    resampler.SetOutputOrigin(input.GetOrigin())
    resampler.SetOutputDirection(input.GetDirection())
    resampler.SetTransform(sitk.Transform())
    resampler.SetDefaultPixelValue(0)

    # 解像度を変更した画像を生成
    return resampler.Execute(input)
