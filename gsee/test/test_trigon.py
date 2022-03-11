import datetime
import math
import os

import pandas as pd
import pytest  # pylint: disable=unused-import

import gsee.trigon


@pytest.fixture
def coords_and_datetimes():
    coords = (47.36, 8.55)  # Zurich, Switzerland
    datetimes = pd.date_range("2000-01-01 00:00", "2000-12-31 23:00", freq="1H")
    return coords, datetimes


@pytest.fixture
def irradiance():
    in_path = os.path.join(os.path.dirname(__file__), "test_irradiance.csv")
    return pd.read_csv(in_path, index_col=0, parse_dates=True)


def test_sun_rise_set_times(coords_and_datetimes):
    coords, datetimes = coords_and_datetimes
    rise_set_times = gsee.trigon.sun_rise_set_times(datetimes, coords)

    assert isinstance(rise_set_times, pd.Series)

    assert len(rise_set_times) == len(datetimes) / 24

    datetimes_01_01 = [
        datetime.replace(microsecond=0) for datetime in rise_set_times.loc["2000-01-01"]
    ]
    datetimes_07_15 = [
        datetime.replace(microsecond=0) for datetime in rise_set_times.loc["2000-07-15"]
    ]

    assert datetimes_01_01[0] == datetime.datetime(2000, 1, 1, 7, 12, 40)
    assert datetimes_01_01[1] == datetime.datetime(2000, 1, 1, 15, 45, 38)

    assert datetimes_07_15[0] == datetime.datetime(2000, 7, 15, 3, 44, 19)
    assert datetimes_07_15[1] == datetime.datetime(2000, 7, 15, 19, 18, 38)


def test_sun_angles(coords_and_datetimes):
    coords, datetimes = coords_and_datetimes
    angles = gsee.trigon.sun_angles(datetimes, coords)

    assert angles.sum()["sun_alt"] == pytest.approx(2127.154644)
    assert angles.sum()["sun_azimuth"] == pytest.approx(15224.532375)

    assert angles.loc["2000-01-01 07:00:00", "duration"] == pytest.approx(47.3333333)
    assert angles.loc["2000-01-01 12:00:00", "duration"] == pytest.approx(60)
    assert angles.loc["2000-01-01 15:00:00", "duration"] == pytest.approx(45.6333333)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ((math.radians(90), math.radians(0), math.radians(0), math.radians(45)), 0),
        ((math.radians(45), math.radians(5), math.radians(0), math.radians(0)), 40),
        ((math.radians(0), math.radians(0), math.radians(0), math.radians(45)), 45),
        ((math.radians(45), math.radians(0), math.radians(90), math.radians(90)), 45),
        ((math.radians(45), math.radians(5), math.radians(180), math.radians(0)), 50),
    ],
)
def test_incidence_single_tracking(test_input, expected):
    result = math.degrees(gsee.trigon._incidence_single_tracking(*test_input))
    assert result == pytest.approx(expected)


def test_aperture_irradiance_dni_only(irradiance, coords_and_datetimes):
    coords = coords_and_datetimes[0]
    direct, diffuse = irradiance["direct"], irradiance["diffuse"]
    result = gsee.trigon.aperture_irradiance(direct, diffuse, coords, dni_only=True)
    assert isinstance(result, pd.Series)
    assert result.mean() == pytest.approx(260.940362)
    assert result.loc["2000-12-31 12:00:00"] == pytest.approx(1448.694722)


def _aperture_irradiance(
    irradiance,
    coords_and_datetimes,
    tracking,
    tilt=math.radians(30),
    azimuth=math.radians(180),
):
    coords = coords_and_datetimes[0]
    direct, diffuse = irradiance["direct"], irradiance["diffuse"]
    result = gsee.trigon.aperture_irradiance(
        direct, diffuse, coords, tilt=tilt, azimuth=azimuth, tracking=tracking
    )
    return result


def test_aperture_irradiance_tracking_0(irradiance, coords_and_datetimes):
    result = _aperture_irradiance(irradiance, coords_and_datetimes, tracking=0)
    assert isinstance(result, pd.DataFrame)
    assert result.mean()["direct"] == pytest.approx(185.266330)
    assert result.mean()["diffuse"] == pytest.approx(59.506055)


def test_aperture_irradiance_tracking_1_horizontal(irradiance, coords_and_datetimes):
    result = _aperture_irradiance(irradiance, coords_and_datetimes, tracking=1, tilt=0)
    assert isinstance(result, pd.DataFrame)
    assert result.mean()["direct"] == pytest.approx(200.394662)
    assert result.mean()["diffuse"] == pytest.approx(57.748641)


def test_aperture_irradiance_tracking_1_30deg(irradiance, coords_and_datetimes):
    result = _aperture_irradiance(
        irradiance, coords_and_datetimes, tracking=1, tilt=math.radians(30)
    )
    assert isinstance(result, pd.DataFrame)
    assert result.mean()["direct"] == pytest.approx(242.210095)
    assert result.mean()["diffuse"] == pytest.approx(57.851825)


def test_aperture_irradiance_tracking_2(irradiance, coords_and_datetimes):
    result = _aperture_irradiance(irradiance, coords_and_datetimes, tracking=2)
    assert isinstance(result, pd.DataFrame)
    assert result.mean()["direct"] == pytest.approx(260.944585)
    assert result.mean()["diffuse"] == pytest.approx(58.169813)
    assert result.loc["2000-12-31 12:00:00", "direct"] == pytest.approx(1448.694722)
