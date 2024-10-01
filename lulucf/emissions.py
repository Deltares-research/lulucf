import itertools

import geopandas as gpd
import numpy as np
import xarray as xr

from lulucf.area_statistics import areal_percentage_bgt_soilmap, calculate_model_flux
from lulucf.lasso import LassoGrid
from lulucf.preprocessing import calc_somers_emission_per_m2, group_soilmap_units
from lulucf.utils import _add_layer_idx_column

MAIN_SOILMAP_UNITS = ["peat", "moerig", "buried", "other"]
MAIN_BGT_UNITS = [
    "pand",
    "wegdeel",
    "waterdeel",
    "ondersteunendwegdeel",
    "ondersteunendwaterdeel",
    "begroeidterreindeel",
    "onbegroeidterreindeel",
    "scheiding",
    "overigbouwwerk",
]


def _combine_bgt_soilmap_names(bgt_layers, soilmap_layers):
    return [f"{b}_{s}" for s, b in itertools.product(soilmap_layers, bgt_layers)]


def calculate_somers_emissions(
    somers: gpd.GeoDataFrame,
    grid: LassoGrid,
):
    """
    Calculate a weighted greenhouse gas flux per cell in a 2D grid from Somers emission
    data.

    Parameters
    ----------
    somers : gpd.GeoDataFrame
        _description_
    grid : LassoGrid
        _description_

    Returns
    -------
    _type_
        _description_
    """
    somers["flux_m2"] = calc_somers_emission_per_m2(somers)
    flux_per_m2 = calculate_model_flux(somers, grid)
    return flux_per_m2


def bgt_soilmap_coverage(
    bgt: gpd.GeoDataFrame, soilmap: gpd.GeoDataFrame, grid: LassoGrid
) -> xr.DataArray:
    """
    Calculate per cell in a grid for each combination of BGT and Soil Map polygons what
    percentage of a cell is covered by the combination. This returns a 3D DataArray with
    dimensions ('y', 'x', 'layer') where the dimension 'layer' contains ordered BGT-Soilmap
    layer combinations.

    Parameters
    ----------
    grid : lulucf.LassoGrid
        LassoGrid instance containing the raster grid to calculate the percentages for.
    bgt : gpd.GeoDataFrame
        GeoDataFrame containing the BGT data polygons.
    soilmap : gpd.GeoDataFrame
        GeoDataFrame containing the BGT data polygons.

    Returns
    -------
    xr.DataArray
        3D DataArray with the areal percentages.

    """
    soilmap = group_soilmap_units(soilmap)

    bgt = _add_layer_idx_column(bgt, MAIN_BGT_UNITS)
    soilmap = _add_layer_idx_column(soilmap, MAIN_SOILMAP_UNITS)

    area = areal_percentage_bgt_soilmap(
        grid, bgt, soilmap, MAIN_BGT_UNITS, MAIN_SOILMAP_UNITS
    )
    layers_area = _combine_bgt_soilmap_names(MAIN_BGT_UNITS, MAIN_SOILMAP_UNITS)
    xco = grid.xcoordinates()
    yco = grid.ycoordinates()

    area = xr.DataArray(
        area.reshape(len(yco), len(xco), len(layers_area)),
        coords={"y": yco, "x": xco, "layer": layers_area},
        dims=("y", "x", "layer"),
    )
    return area
