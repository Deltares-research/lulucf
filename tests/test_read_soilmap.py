import geopandas as gpd
import pytest

from lulucf.readers import BroSoilmap, read_soilmap_geopackage


class TestBroSoilmap:
    @pytest.mark.unittest
    def test_read_geometries(self, simple_soilmap_path):
        with BroSoilmap(simple_soilmap_path) as sm:
            soilmap = sm.read_geometries()
            assert isinstance(soilmap, gpd.GeoDataFrame)


@pytest.mark.unittest
def test_read_soilmap_geopackage(simple_soilmap_path):
    soilmap = read_soilmap_geopackage(simple_soilmap_path)
    assert isinstance(soilmap, gpd.GeoDataFrame)

    expected_columns = ["maparea_id", "soilunit_code"]
    assert all([col in soilmap.columns for col in expected_columns])
