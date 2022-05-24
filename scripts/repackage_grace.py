""" Repackage the GRACE follow-on data to a more efficient format. 

"""
import os
import glob
import csv
from astropy.time import Time
import pandas as pd
import xarray as xr


data_folder = "/home/cedric/PHD/Dev/AnomalPy/Data/GRACE/"


col_names = ["MJD", "frac. of a day", "GPS range AB [m]",
        "GPS range rate AB [m/s]", "Kband range [m]",
        "Kband range rate [m/s]", "O-C range rate [m/s]", 
        "Latitude [°]", "Longitude [°]", "Arg. of lat. [°]", "beta [°]"]

# Read and concatenate all dataframes.
dfs = []
for path in glob.glob(os.path.join(data_folder, "dataset_residuals_operationalSolution/*/*.RES")):
        dfs.append(pd.read_csv(path, sep="\s+", skiprows=12, names=col_names))

df = pd.concat(dfs)

# Convert times from modified Julian to datetime.
df['time'] = Time(df["MJD"] + df["frac. of a day"], format="mjd")
df.set_index("time")

# Use xarray to store in Zarr.
# Also chunk data so can load partially.
ds = xr.Dataset.from_dataframe(df)
ds = ds.chunk(25000)

# Save to zarr format.
ds.to_zarr(os.path.join(data_folder, "./GRACE_merged_2019.zarr"), mode='w')
