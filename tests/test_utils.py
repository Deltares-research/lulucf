import sqlite3

import pytest
from shapely.geometry import Polygon

from lulucf.utils import cell_as_geometry, create_connection


@pytest.fixture
def cellsize_negative_y():
    return (1, -1)


@pytest.fixture
def cellsize_negative_x():
    return (-1, 1)


@pytest.fixture
def cellsize_positive():
    return (1, 1)


@pytest.mark.parametrize(
    "cellsize", ["cellsize_negative_y", "cellsize_negative_x", "cellsize_positive"]
)
def test_cell_as_geometry(cellsize, request):
    cellsize = request.getfixturevalue(cellsize)

    xcell = 1.5
    ycell = 1.5

    geom = cell_as_geometry(xcell, ycell, cellsize)

    assert isinstance(geom, Polygon)
    assert geom.bounds == (1, 1, 2, 2)


@pytest.mark.unittest
def test_create_connection(simple_soilmap_path):
    conn = create_connection(simple_soilmap_path)
    assert isinstance(conn, sqlite3.Connection)
