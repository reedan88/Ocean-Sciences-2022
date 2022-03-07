#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import os
import re
import xarray as xr

# Setup some attributes, used to replace those incorrectly set, or needed after the processing below
ATTRS = {
    'unique_id': {
        'long_name': 'Instrument Unique ID',
        'comment': ('One byte checksum summary of the instrument serial number, name, calibration date and firmware '
                    'version serving as a proxy for a unique ID. While identified as the instrument unique ID, it is '
                    'possible for more than one instrument to have the same checksum summary. Thus, the uniqueness '
                    'of this value should be considered with a certain degree of caution.'),
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'measurements': {
        'long_name': 'Measurements Array',
        'comment': 'Dimensional indexing array created for the light measurements.',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'blanks': {
        'long_name': 'Blanks Array',
        'comment': 'Dimensional indexing array created for the reference (blanks) measurements.',
        # 'units': ''    # deliberately left blank, no units for this value
    },
    'blank_refrnc_434': {
        'long_name': 'DI Blank Reference Intensity at 434 nm',
        'comment': ('Optical absorbance reference intensity at 434 nm. Measured with deionized water. Reference and '
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower '
                    'intensities will result in higher noise in the absorbance and pH measurements. Obtained from '
                    'the reference_light_measurements variable in the Data Portal sourced data file.'),
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'blank_signal_434': {
        'long_name': 'DI Blank Signal Intensity at 434 nm',
        'comment': ('Optical absorbance signal intensity at 434 nm. Measured with deionized water. Reference and '
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower '
                    'intensities will result in higher noise in the absorbance and pH measurements. Obtained from '
                    'the reference_light_measurements variable in the Data Portal sourced data file.'),
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'blank_refrnc_578': {
        'long_name': 'DI Blank Reference Intensity at 578 nm',
        'comment': ('Optical absorbance reference intensity at 578 nm. Measured with deionized water. Reference and '
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower '
                    'intensities will result in higher noise in the absorbance and pH measurements. Obtained from '
                    'the reference_light_measurements variable in the Data Portal sourced data file.'),
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'blank_signal_578': {
        'long_name': 'DI Blank Signal Intensity at 578 nm',
        'comment': ('Optical absorbance signal intensity at 578 nm. Measured with deionized water. Reference and '
                    'signal intensities range between 0 and 4096. Values should be greater than ~1500. Lower '
                    'intensities will result in higher noise in the absorbance and pH measurements. Obtained from '
                    'the reference_light_measurements variable in the Data Portal sourced data file.'),
        'units': 'counts',
        '_FillValue': -9999999,
    },
    'reference_434': {
        'long_name': 'Reference Intensity at 434 nm',
        'comment': ('Optical absorbance reference intensity at 434 nm. Reference and signal intensities range '
                    'between 0 and 4096. Values should be greater than ~1500. Lower intensities will result in '
                    'higher noise in the absorbance and pH measurements. Obtained from the light_measurements'
                    'variable in the Data Portal sourced data file.'),
        'units': 'counts'
    },
    'signal_434': {
        'long_name': 'Signal Intensity at 434 nm',
        'comment': ('Optical absorbance signal intensity at 434 nm. Reference and signal intensities range between 0 '
                    'and 4096. Values should be greater than ~1500. Lower intensities will result in higher noise in '
                    'the absorbance and pH measurements. Obtained from the light_measurements variable in the Data '
                    'Portal sourced data file.'),
        'data_product_identifier': 'PH434SI_L0',
        'units': 'counts'
    },
    'reference_578': {
        'long_name': 'Reference Intensity at 578 nm',
        'comment': ('Optical absorbance reference intensity at 578 nm. Reference and signal intensities range '
                    'between 0 and 4096. Values should be greater than ~1500. Lower intensities will result in '
                    'higher noise in the absorbance and pH measurements. Obtained from the light_measurements '
                    'variable in the Data Portal sourced data file.'),
        'units': 'counts'
    },
    'signal_578': {
        'long_name': 'Signal Intensity at 578 nm',
        'comment': ('Optical absorbance signal intensity at 578 nm. Reference and signal intensities range between 0 '
                    'and 4096. Values should be greater than ~1500. Lower intensities will result in higher noise in '
                    'the absorbance and pH measurements. Obtained from the light_measurements variable in the Data '
                    'Portal sourced data file.'),
        'data_product_identifier': 'PH578SI_L0',
        'units': 'counts'
    },
    'raw_thermistor_start': {
        'long_name': 'Raw Thermistor Temperature, Measurement Start',
        'comment': 'Thermistor resistivity measured in counts at the start of the measurement cycle.',
        'units': 'counts'
    },
    'raw_thermistor_end': {
        'long_name': 'Raw Thermistor Temperature, Measurement End',
        'comment': 'Thermistor resistivity measured in counts at the end of the measurement cycle.',
        'units': 'counts'
    },
    'raw_battery_voltage': {
        'long_name': 'Raw Battery Voltage',
        'comment': ('Raw internal battery voltage measured in counts. May actually reflect external voltage if '
                    'external power is applied'),
        'units': 'counts'
    },
    'thermistor_temperature': {
        'long_name': 'Thermistor Temperature',
        'comment': ('Thermistor temperature refers to the internal instrument temperature of the pH sensor, as '
                    'measured by the thermistor. It is used to determine salinity and temperature dependent molar '
                    'absorptivities in the seawater sample in order to make an accurate pH estimation. This '
                    'variable represents the thermistor temperature measured at the end of the measurement cycle'),
        'units': 'degrees_Celsius',
        'ancillary_variables': 'raw_thermistor_end'
    },
    'seawater_ph': {
        'long_name': 'Seawater pH',
        'comment': ('pH is a measurement of the concentration of hydrogen ions in a solution. pH ranges from acidic '
                    'to basic on a scale from 0 to 14 with 7 being neutral.'),
        'standard_name': 'sea_water_ph_reported_on_total_scale',
        'data_product_identifier': 'PHWATER_L2',
        # 'units': ''    # deliberately left blank, no units for this value
        'ancillary_variables': ('blank_refrnc_434 blank_signal_434 blank_refrnc_578 blank_signal_578 '
                                'reference_434 signal_434 reference_578 signal_578 thermistor_temperature '
                                'practical_salinity seawater_ph_quality_flag')
    },
    'seawater_ph_quality_flag': {
        'long_name': 'Seawater pH Quality Flag',
        'comment': ('Quality assessment of the seawater pH based on assessments of the raw values used to calculate '
                    'the pH. Levels used to indicate failed quality are pulled from the vendor code. Suspect values '
                    'are flagged based on past instrument performance.'),
        'standard_name': 'sea_water_ph_reported_on_total_scale status_flag',
        'flag_values': np.array([1, 2, 3, 4, 9], dtype=np.int32),
        'flag_meanings': 'pass not_evaluated suspect_or_of_high_interest fail missing_data',
        # 'units': ''    # deliberately left blank, no units for this value
        'ancillary_variables': ('blank_signal_434 blank_signal_578 signal_434 reference_434 signal_578 '
                                'reference_578 seawater_ph')
    }
}


def dt64_epoch(dt64):
    """
    Convert a panda or xarray date/time value represented as a datetime64 object (nanoseconds since 1970) to a float,
    representing an epoch time stamp (seconds since 1970-01-01).

    :param dt64: panda or xarray datatime64 object
    :return epts: epoch time as seconds since 1970-01-01
    """
    epts = dt64.values.astype(float) / 10.0 ** 9
    return epts


def quality_checks(ds):
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


def phsen_datalogger(ds):
    """
    Takes PHSEN data recorded by the data loggers used in the CGSN/EA moorings
    and cleans up the data set to make it more user-friendly. Primary task is
    renaming parameters and dropping some that are of limited use. Additionally,
    re-organize some of the variables to permit better assessments of the data.

    :param ds: initial PHSEN data set recorded by the data logger system and
        downloaded from OOI via the M2M system
    :return: cleaned up and reorganized data set
    """
    # drop some of the variables:
    #   passed_checksum == not used
    #   record_type == not used
    #   record_time == not used
    #   dcl_controller_timestamp == time, redundant so can remove
    #   phsen_abcdef_signal_intensity_434, part of the light measurements array, redundant so can remove
    #   phsen_abcdef_signal_intensity_578, part of the light measurements array, redundant so can remove
    ds = ds.reset_coords()
    drop_vars = ['passed_checksum', 'record_type', 'record_time', 'phsen_abcdef_signal_intensity_434',
                  'phsen_abcdef_signal_intensity_578', 'dcl_controller_timestamp']
    for var in ds.variables:
        if var in drop_vars:
            ds = ds.drop(var)

    # convert the time values from a datetime64[ns] object to a floating point number with the time in seconds
    try:
        ds['internal_timestamp'] = ('time', dt64_epoch(ds.internal_timestamp))
        ds['internal_timestamp'].attrs = dict({
            'long_name': 'Internal SAMI-pH Clock Time',
            'standard_name': 'time',
            'units': 'seconds since 1970-01-01 00:00:00 0:00',
            'calendar': 'gregorian',
            'comment': ('Comparing the instrument internal clock versus the GPS referenced sampling time will allow for ' +
                        'calculations of the instrument clock offset and drift. Useful when working with the ' +
                        'recovered instrument data where no external GPS referenced clock is available.')
        })
    except:
        pass

    # rename some of the variables for better clarity
    rename = {
        'voltage_battery': 'raw_battery_voltage',
        'thermistor_start': 'raw_thermistor_start',
        'thermistor_end': 'raw_thermistor_end',
        'phsen_thermistor_temperature': 'thermistor_temperature',
        'phsen_abcdef_ph_seawater': 'seawater_ph',
        'phsen_abcdef_ph_seawater_qc_executed': 'seawater_ph_qc_executed',
        'phsen_abcdef_ph_seawater_qc_results': 'seawater_ph_qc_results'
    }
    ds = ds.rename(rename)

    # now we need to reset the light and reference arrays to named variables that will be more meaningful and useful in
    # the final data files
    nrec = len(ds['time'].values)
    light = np.array(np.vstack(ds['light_measurements'].values), dtype='int32')
    light = np.atleast_3d(light)
    light = np.reshape(light, (nrec, 23, 4))  # 4 sets of 23 seawater measurements
    reference_434 = light[:, :, 0]            # reference signal, 434 nm
    signal_434 = light[:, :, 1]               # signal intensity, 434 nm (PH434SI_L0)
    reference_578 = light[:, :, 2]            # reference signal, 578 nm
    signal_578 = light[:, :, 3]               # signal intensity, 578 nm (PH578SI_L0)

    refnc = np.array(np.vstack(ds['reference_light_measurements'].values), dtype='int32')
    refnc = np.atleast_3d(refnc)
    refnc = np.reshape(refnc, (nrec, 4, 4))   # 4 sets of 4 DI water measurements (blanks)
    blank_refrnc_434 = refnc[:, :, 0]  # DI blank reference, 434 nm
    blank_signal_434 = refnc[:, :, 1]  # DI blank signal, 434 nm
    blank_refrnc_578 = refnc[:, :, 2]  # DI blank reference, 578 nm
    blank_signal_578 = refnc[:, :, 3]  # DI blank signal, 578 nm

    # create a data set with the reference and light measurements
    ph = xr.Dataset({
        'blank_refrnc_434': (['time', 'blanks'], blank_refrnc_434.astype('int32')),
        'blank_signal_434': (['time', 'blanks'], blank_signal_434.astype('int32')),
        'blank_refrnc_578': (['time', 'blanks'], blank_refrnc_578.astype('int32')),
        'blank_signal_578': (['time', 'blanks'], blank_signal_578.astype('int32')),
        'reference_434': (['time', 'measurements'], reference_434.astype('int32')),
        'signal_434': (['time', 'measurements'], signal_434.astype('int32')),
        'reference_578': (['time', 'measurements'], reference_578.astype('int32')),
        'signal_578': (['time', 'measurements'], signal_578.astype('int32'))
    }, coords={'time': ds['time'], 'measurements': np.arange(0, 23).astype('int32'),
               'blanks': np.arange(0, 4).astype('int32')
               })
    ds = ds.drop(['reference_light_measurements_dim_0', 'spectrum', 'light_measurements',
                  'reference_light_measurements'])

    # these two dimensional variables may or may not be present depending on how the data was requested.
    # remove them if they do exist so we can merge different data sets together
    maybe = ['phsen_abcdef_signal_intensity_434_dim_0', 'phsen_abcdef_signal_intensity_578_dim_0']
    for k, v in ds.dims.items():
        if k in maybe:
            ds = ds.drop(k)

    # merge the data sets back together
    ds = ds.merge(ph)

    # test data quality
    ds['seawater_ph_quality_flag'] = quality_checks(ds)

    # reset some attributes
    for key, value in ATTRS.items():
        for atk, atv in value.items():
            if key in ds.variables:
                ds[key].attrs[atk] = atv

    # add the original variable name as an attribute, if renamed
    for key, value in rename.items():
        ds[value].attrs['ooinet_variable_name'] = key

    # and reset some of the data types
    data_types = ['deployment', 'raw_thermistor_end', 'raw_thermistor_start', 'unique_id', 'raw_battery_voltage']
    for v in data_types:
        ds[v] = ds[v].astype('int32')

    return ds


def phsen_instrument(ds):
    """
    Takes PHSEN data recorded by internally by the instrument, and cleans up
    the data set to make it more user-friendly. Primary task is renaming
    parameters and dropping some that are of limited use. Additionally,
    re-organize some of the variables to permit better assessments of the data.


    :param ds: initial PHSEN data set recorded internally by the instrument and
        downloaded from OOI via the M2M system
    :return: cleaned up data set
    """
    # drop some of the variables:
    #   record_type == not used
    #   record_time == internal_timestamp == time, redundant so can remove both
    ds = ds.reset_coords()
    drop_vars = ['record_type', 'record_time', 'internal_timestamp']
    for var in ds.variables:
        if var in drop_vars:
            ds = ds.drop(var)

    # rename some of the variables for better clarity
    rename = {
        'voltage_battery': 'raw_battery_voltage',
        'thermistor_start': 'raw_thermistor_start',
        'thermistor_end': 'raw_thermistor_end',
        'phsen_thermistor_temperature': 'thermistor_temperature',
        'phsen_abcdef_ph_seawater': 'seawater_ph',
        'phsen_abcdef_ph_seawater_qc_executed': 'seawater_ph_qc_executed',
        'phsen_abcdef_ph_seawater_qc_results': 'seawater_ph_qc_results'
    }
    ds = ds.rename(rename)

    # now we need to reset the light and reference arrays to named variables that will be more meaningful and useful in
    # the final data files
    nrec = len(ds['time'].values)
    light = np.array(np.vstack(ds['light_measurements'].values), dtype='int32')
    light = np.atleast_3d(light)
    light = np.reshape(light, (nrec, 23, 4))  # 4 sets of 23 seawater measurements
    reference_434 = light[:, :, 0]            # reference signal, 434 nm
    signal_434 = light[:, :, 1]               # signal intensity, 434 nm (PH434SI_L0)
    reference_578 = light[:, :, 2]            # reference signal, 578 nm
    signal_578 = light[:, :, 3]               # signal intensity, 578 nm (PH578SI_L0)

    refnc = np.array(np.vstack(ds['reference_light_measurements'].values), dtype='int32')
    refnc = np.atleast_3d(refnc)
    refnc = np.reshape(refnc, (nrec, 4, 4))   # 4 sets of 4 DI water measurements (blanks)
    blank_refrnc_434 = refnc[:, :, 0]  # DI blank reference, 434 nm
    blank_signal_434 = refnc[:, :, 1]  # DI blank signal, 434 nm
    blank_refrnc_578 = refnc[:, :, 2]  # DI blank reference, 578 nm
    blank_signal_578 = refnc[:, :, 3]  # DI blank signal, 578 nm

    # create a data set with the reference and light measurements
    ph = xr.Dataset({
        'blank_refrnc_434': (['time', 'blanks'], blank_refrnc_434.astype('int32')),
        'blank_signal_434': (['time', 'blanks'], blank_signal_434.astype('int32')),
        'blank_refrnc_578': (['time', 'blanks'], blank_refrnc_578.astype('int32')),
        'blank_signal_578': (['time', 'blanks'], blank_signal_578.astype('int32')),
        'reference_434': (['time', 'measurements'], reference_434.astype('int32')),
        'signal_434': (['time', 'measurements'], signal_434.astype('int32')),
        'reference_578': (['time', 'measurements'], reference_578.astype('int32')),
        'signal_578': (['time', 'measurements'], signal_578.astype('int32'))
    }, coords={'time': ds['time'], 'measurements': np.arange(0, 23).astype('int32'),
               'blanks': np.arange(0, 4).astype('int32')
               })
    ds = ds.drop(['light_measurements', 'reference_light_measurements', 'spectrum',
                  'reference_light_measurements_dim_0'])

    # these two dimensional variables may or may not be present depending on how the data was requested.
    # remove them if they do exist so we can merge different data sets together
    maybe = ['phsen_abcdef_signal_intensity_434_dim_0', 'phsen_abcdef_signal_intensity_578_dim_0']
    for k, v in ds.dims.items():
        if k in maybe:
            ds = ds.drop(k)

    # merge the data sets back together
    ds = ds.merge(ph)

    # test data quality
    ds['seawater_ph_quality_flag'] = quality_checks(ds)

    # reset some attributes
    for key, value in ATTRS.items():
        for atk, atv in value.items():
            if key in ds.variables:
                ds[key].attrs[atk] = atv

    # add the original variable name as an attribute, if renamed
    for key, value in rename.items():
        ds[value].attrs['ooinet_variable_name'] = key

    # and reset some of the data types
    data_types = ['deployment', 'raw_thermistor_end', 'raw_thermistor_start', 'raw_battery_voltage']
    for v in data_types:
        ds[v] = ds[v].astype('int32')

    return ds


def phsen_imodem(ds):
    """
    Takes PHSEN data recorded by over the inductive modem line, and cleans up
    the data set to make it more user-friendly. Primary task is renaming
    parameters and dropping some that are of limited use. Additionally,
    re-organize some of the variables to permit better assessments of the data.


    :param ds: initial PHSEN data set recorded internally by the instrument and
        downloaded from OOI via the M2M system
    :return: cleaned up data set
    """
    # drop some of the variables:
    #   passed_checksum == not used
    #   record_type == not used
    #   record_time == internal_timestamp == time, redundant so can remove both
    #   phsen_abcdef_signal_intensity_434, part of the light measurements array, redundant so can remove
    #   phsen_abcdef_signal_intensity_578, part of the light measurements array, redundant so can remove
    ds = ds.reset_coords()
    for variable in ['passed_checksum', 'record_type', 'record_time', 'internal_timestamp',
                     'phsen_abcdef_signal_intensity_434', 'phsen_abcdef_signal_intensity_578']:
        try:
            ds = ds.drop_vars(variable)
        except:
            pass

    # rename some of the variables for better clarity
    rename = {
        'voltage_battery': 'raw_battery_voltage',
        'thermistor_start': 'raw_thermistor_start',
        'thermistor_end': 'raw_thermistor_end',
        'phsen_thermistor_temperature': 'thermistor_temperature',
        'phsen_abcdef_ph_seawater': 'seawater_ph',
        'phsen_abcdef_ph_seawater_qc_executed': 'seawater_ph_qc_executed',
        'phsen_abcdef_ph_seawater_qc_results': 'seawater_ph_qc_results'
    }
    ds = ds.rename(rename)

    # now we need to reset the light and reference arrays to named variables that will be more meaningful and useful in
    # the final data files
    nrec = len(ds['time'].values)
    light = np.array(np.vstack(ds['light_measurements'].values), dtype='int32')
    light = np.atleast_3d(light)
    light = np.reshape(light, (nrec, 23, 4))  # 4 sets of 23 seawater measurements
    reference_434 = light[:, :, 0]            # reference signal, 434 nm
    signal_434 = light[:, :, 1]               # signal intensity, 434 nm (PH434SI_L0)
    reference_578 = light[:, :, 2]            # reference signal, 578 nm
    signal_578 = light[:, :, 3]               # signal intensity, 578 nm (PH578SI_L0)

    refnc = np.array(np.vstack(ds['reference_light_measurements'].values), dtype='int32')
    refnc = np.atleast_3d(refnc)
    refnc = np.reshape(refnc, (nrec, 4, 4))   # 4 sets of 4 DI water measurements (blanks)
    blank_refrnc_434 = refnc[:, :, 0]  # DI blank reference, 434 nm
    blank_signal_434 = refnc[:, :, 1]  # DI blank signal, 434 nm
    blank_refrnc_578 = refnc[:, :, 2]  # DI blank reference, 578 nm
    blank_signal_578 = refnc[:, :, 3]  # DI blank signal, 578 nm

    # create a data set with the reference and light measurements
    ph = xr.Dataset({
        'blank_refrnc_434': (['time', 'blanks'], blank_refrnc_434.astype('int32')),
        'blank_signal_434': (['time', 'blanks'], blank_signal_434.astype('int32')),
        'blank_refrnc_578': (['time', 'blanks'], blank_refrnc_578.astype('int32')),
        'blank_signal_578': (['time', 'blanks'], blank_signal_578.astype('int32')),
        'reference_434': (['time', 'measurements'], reference_434.astype('int32')),
        'signal_434': (['time', 'measurements'], signal_434.astype('int32')),
        'reference_578': (['time', 'measurements'], reference_578.astype('int32')),
        'signal_578': (['time', 'measurements'], signal_578.astype('int32'))
    }, coords={'time': ds['time'], 'measurements': np.arange(0, 23).astype('int32'),
               'blanks': np.arange(0, 4).astype('int32')
               })
    ds = ds.drop(['light_measurements', 'reference_light_measurements', 'spectrum',
                  'reference_light_measurements_dim_0'])

    # merge the data sets back together
    ds = ds.merge(ph)

    # test data quality
    ds['seawater_ph_quality_flag'] = quality_checks(ds)

    # reset some attributes
    for key, value in ATTRS.items():
        for atk, atv in value.items():
            if key in ds.variables:
                ds[key].attrs[atk] = atv

    # add the original variable name as an attribute, if renamed
    for key, value in rename.items():
        ds[value].attrs['ooinet_variable_name'] = key

    # and reset some of the data types
    data_types = ['deployment', 'raw_thermistor_end', 'raw_thermistor_start', 'raw_battery_voltage']
    for v in data_types:
        ds[v] = ds[v].astype('int32')

    return ds
