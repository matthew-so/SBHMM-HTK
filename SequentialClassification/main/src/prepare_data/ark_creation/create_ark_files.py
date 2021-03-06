"""Creates .ark files needed as intermediate step to creating .htk files

Methods
-------
_create_ark_file
create_ark_files
"""
import os
import glob
import shutil
import tqdm

import pandas as pd

from .feature_selection import select_features
from .interpolate_feature_data import interpolate_feature_data


def _create_ark_file(df: pd.DataFrame, ark_filepath: str, title: str) -> None:
    """Creates a single .ark file

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing selected feature.

    ark_filepath : str
        File path at which to save .ark file.

    title : str
        Title containing label needed as header of .ark file.
    """

    with open(ark_filepath, 'w') as out:
        out.write('{} [ '.format(title))
        
    df.to_csv(ark_filepath, mode='a', header=False, index=False, sep=' ')

    with open(ark_filepath, 'a') as out:
        out.write(']')


def create_ark_files(features_config: dict, verbose: bool = False, is_select_features: bool = False) -> None:
    """Creates .ark files needed as intermediate step to creating .htk
    files

    Parameters
    ----------
    features_config : dict
        Contains features_dir and features_to_extract

    verbose : bool, optional, by default False
        Whether to print output during process.
    """

    ark_dir = os.path.join('data', 'ark')

    if os.path.exists(ark_dir):
        shutil.rmtree(ark_dir)

    os.makedirs(ark_dir)
        
    features_filepaths = glob.glob(features_config['features_dir'])

    if is_select_features:
        print("select_features data")
    else:
        print("interpolate_features data")

    for features_filepath in tqdm.tqdm(features_filepaths):

        if verbose:
            print(features_filepath)
        
        if is_select_features:
            features_df = select_features(features_filepath, features_config['selected_features']) # Interpolation (mediapipe.data filepath, features to extract)
        else:
            features_df = interpolate_feature_data(features_filepath, features_config['selected_features']) # Interpolation (mediapipe.data filepath, features to extract)

        if features_df is not None:
            ark_filename = features_filepath.split('/')[-1].replace('data', 'ark')
            ark_filepath = os.path.join(ark_dir, ark_filename)
            title = ark_filename.replace('.ark', "")
            _create_ark_file(features_df, ark_filepath, title)