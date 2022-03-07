# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import numpy as np
import os
import re
import xarray as xr
import haversine as hs
import matplotlib.pyplot as plt
from ast import literal_eval


def findNearest(bottleData, buoyLoc, maxDist):
    """Find the bottle sample values within a maximum distance from the buoy
    
    Parameters
    ----------
    bottleData: (pd.DataFrame -> strings or floats)
        A tuple of (latitude, longitude) values in decimal degrees of the bottle sample location
    buoyLoc: (tuple -> floats)
        A tuple of (latitude, longitude) values in decimal degrees of the buoy location
    maxDist: (float)
        Maximum distance in km away for a sample location from the buoy location
    
    Returns
    -------
    mask: (boolean)
        Returns True or False boolean if sampleLoc < maxDist from buoyLoc
    """
    # Get the startLat/startLon as floats
    startLat = bottleData["Start Latitude [degrees]"].apply(lambda x: float(x))
    startLon = bottleData["Start Longitude [degrees]"].apply(lambda x: float(x))
    
    # Calculate the distance
    distance = []
    for lat, lon in zip(startLat, startLon):
        sampleLoc = (lat, lon)
        distance.append(hs.haversine(sampleLoc, buoyLoc))
    
    # Filter the results
    return [d <= maxDist for d in distance]


def findSamples(bottleData, buoyLoc, buoyDepth, maxDist, depthTol):
    
    """Find the bottle sample values within a maximum distance from the buoy
    
    Parameters
    ----------
    bottleData: (pd.DataFrame -> strings or floats)
        A tuple of (latitude, longitude) values in decimal degrees of the bottle sample location
    buoyLoc: (tuple -> floats)
        A tuple of (latitude, longitude) values in decimal degrees of the buoy location
    buoyDepth: (float)
        Deployment depth of the instrument
    maxDist: (float)
        Maximum distance in km away for a sample location from the buoy location
    depthTol: (float)
        Maximum depth difference to select samples from the buoyDepth
    
    Returns
    -------
    mask: (boolean)
        Returns True or False boolean if sampleLoc < maxDist from buoyLoc
    """
    # Filter for the nearest samples
    nearest = findNearest(bottleData, buoyLoc, maxDist)
    bottleData = bottleData[nearest]
    
    # Filter based on depth
    depthMin = buoyDepth - depthTol
    depthMax = buoyDepth + depthTol
    bottleData = bottleData[(bottleData["CTD Depth [m]"] >= depthMin) & (bottleData["CTD Depth [m]"] <= depthMax)]
    
    return bottleData


def phsen_quality_checks(ds):
    """
    Assessment of the raw data and the calculated seawater pH for quality
    using a susbset of the QARTOD flags to indicate the quality. QARTOD
    flags used are:
        1 = Pass
        3 = Suspect or of High Interest
        4 = Fail
    Suspect flags are set based on experience with the instrument and the data
    produced by it. Failed flags are based on code provided by the vendor. The
    final flag value represents the worst case assessment of the data quality.
    :param ds: xarray dataset with the raw signal data and the calculated
               seawater pH
    :return qc_flag: array of flag values indicating seawater pH quality
    """
    max_bits = 4096                                # max measurement value
    qc_flag = ds['time'].astype('int32') * 0 + 1   # default flag values, no errors

    # test suspect indicator signals -- values starting to get too low for a good calculation
    m434 = ds.signal_434 < max_bits / 12  # value based on what would be considered too low for blanks
    m578 = ds.signal_578 < max_bits / 12  # value based on what would be considered too low for blanks
    m = np.any([m434.all(axis=1), m578.all(axis=1)], axis=0)
    qc_flag[m] = 3

    # test suspect flat indicator signals -- indicates pump might be starting to fail or otherwise become obstructed.
    m434 = ds.signal_434.std(axis=1) < 180  # test level is 3x the fail level
    m578 = ds.signal_578.std(axis=1) < 180  # test level is 3x the fail level
    m = np.any([m434, m578], axis=0)
    qc_flag[m] = 3

    # test for suspect pH values -- user range set to 7.4 and 8.6
    m = (ds.seawater_ph.values < 7.4) | (ds.seawater_ph.values > 8.6)   # from real-world expectations
    qc_flag[m] = 3

    # test for suspect reference measurements -- erratic reference measurements, with larger than usual variability.
    m434 = ds.reference_434.std(axis=1) > 10  # value based on 5x of normal standard deviations
    m578 = ds.reference_578.std(axis=1) > 10  # value based on 5x of normal standard deviations
    m = np.any([m434, m578], axis=0)
    qc_flag[m] = 3

    # test for failed blank measurements -- blank measurements either too high (saturated signal) or too low.
    m434 = (ds.blank_signal_434 > max_bits - max_bits / 20) | (ds.blank_signal_434 < max_bits / 12)
    m578 = (ds.blank_signal_578 > max_bits - max_bits / 20) | (ds.blank_signal_578 < max_bits / 12)
    m = np.any([m434.all(axis=1), m578.all(axis=1)], axis=0)
    qc_flag[m] = 4

    # test for failed intensity measurements -- intensity measurements either too high (saturated signal) or too low.
    m434 = (ds.signal_434 > max_bits - max_bits / 20) | (ds.signal_434 < 5)
    m578 = (ds.signal_578 > max_bits - max_bits / 20) | (ds.signal_578 < 5)
    m = np.any([m434.all(axis=1), m578.all(axis=1)], axis=0)
    qc_flag[m] = 4

    # test for flat intensity measurements -- indicates pump isn't working or the flow cell is otherwise obstructed.
    m434 = ds.signal_434.std(axis=1) < 60
    m578 = ds.signal_578.std(axis=1) < 60
    m = np.any([m434, m578], axis=0)
    qc_flag[m] = 4

    # test for out of range pH values -- sensor range set to 6.9 and 9.0
    m = (ds.seawater_ph.values < 6.9) | (ds.seawater_ph.values > 9.0) | (np.isnan(ds.seawater_ph.values))
    qc_flag[m] = 4

    return qc_flag


def dt64_epoch(dt64):
    """
    Convert a panda or xarray date/time value represented as a datetime64 object (nanoseconds since 1970) to a float,
    representing an epoch time stamp (seconds since 1970-01-01).

    :param dt64: panda or xarray datatime64 object
    :return epts: epoch time as seconds since 1970-01-01
    """
    epts = dt64.values.astype(float) / 10.0 ** 9
    return epts


