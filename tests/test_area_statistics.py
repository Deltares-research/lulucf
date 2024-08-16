import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from lulucf.area_statistics import calculate_areal_percentages_bgt


@pytest.mark.unittest
def test_calculate_areal_percentages_bgt(bgt_gdf, empty_bgt_array):
    result = calculate_areal_percentages_bgt(bgt_gdf, empty_bgt_array)

    assert np.all((result == 0).any(dim="layer"))

    # Test result at sample locations.
    assert_array_almost_equal(
        result[0, 0], [0.00660393, 0.60085776, 0, 0.39253831, 0, 0, 0, 0, 0]
    )
    assert_array_almost_equal(
        result[0, 1], [0.85454545, 0.14545455, 0, 0, 0, 0, 0, 0, 0]
    )
    assert_array_almost_equal(
        result[3, 2], [0, 0, 0, 0, 0, 0.9, 0.1, 0, 0]
    )
