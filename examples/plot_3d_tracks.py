""" Plot satellite tracks in 3D using plotly.

"""
import numpy as np
import xarray as xr


grace_data_path = "/home/cedric/PHD/Dev/AnomalPy/Data/GRACE/GRACE_merged_2019.zarr"
grace_data = xr.open_zarr(grace_data_path).to_dataframe()


# Function for converting spherical coordinates.
def spheric2cartesian(r, theta, phi):
    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z= r * np.cos(phi)
    return x, y, z

grace_data['x'], grace_data['y'], grace_data['z'] = zip(*grace_data.apply(
        lambda x: spheric2cartesian(1, x['Latitude [°]'], x['Longitude [°]']), axis=1))

import plotly.express as px
fig = px.scatter_3d(grace_data[:10000], x="x", y="y", z="z", color="Kband range [m]")
fig.show()

fig = px.scatter_3d(grace_data[:5000], x="x", y="y", z="z", color="O-C range rate [m per s]")
fig.show()
