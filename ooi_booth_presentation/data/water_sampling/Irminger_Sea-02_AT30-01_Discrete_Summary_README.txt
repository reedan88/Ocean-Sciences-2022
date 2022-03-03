# Irminger_Sea-02_AT30-01

---
Author: Andrew Reed <br>
Date: 2021-05-17 <br>
Version: 1-01 <br>
Updates: Fixed column header spellings. Checked format of spreadsheet.

---
Author: Andrew Reed <br>
Date: 2021-01-04 <br>
Version: 1-00 <br>

---
### File Processing<br>
  ##### Methodology
  There should be one row for each station-cast-niskin bottle. Multiple samples for the same
  parameter from a single niskin bottle are split into separate rows, with the associated
  CTD data copied to the new row. The first row of the file is the column headers. <br>

  ##### Notes<br>
  | Station-Cast #  | Bottle Position | Comment |
  | --------------- | --------------- | ------- |
  | 1 | All Bottles | Release test; no samples |
  | 6 | 6, 10 | Duplicate nitrate, chlorophyll |
  | 7 | All Bottles | Confirming water depth; no samples |
  | 11 | 12 | Duplicate chlorophyll |
  | 12 | 12 | Bottle compromised during recovery |

### Salinity<br>

  ##### Methodology<br>
  Salinity measurements are performed following the methodology outlined in the
  WHOI Hydrography Blue Book _Automated Oxygen Titration and Salinity Determination_
  (Knapp et al. 1990). Measurements are performed using a Guildline Autosal model
  8400B salinometer (Guildline Instruments of Canada). Manufacturer stated
  accuracy and precision at 35 psu is +/- 0.003 psu and 0.0002 psu. IAPSO standard
  seawater is used to standardize the Autosal daily before runs.<br>

  #####  Notes<br>
  Nothing to note.

<br>

### Oxygen<br>

  ##### Methodology<br>
  Dissolved oxygen measurements are performed following the methodology outlined
  in the WHOI Hydrography Blue Book _Automated Oxygen Titration and Salinity
  Determination_ (Knapp et al. 1990). Measurements are performed using a Metrohm
  Model 888 Titrando dosing device, with the titration endpoint determined
  amperometrically. Stated accuracy is 0.02 ml/l, with a precision of 0.001 ml/l.<br>

  ##### Notes<br>
  Nothing to note.

<br>

### Nutrients<br>

  ##### Methodology<br>
  All nutrient values are reported as the average of triplicate analysis on a
  single collected sample.

  ##### Notes<br>
  Nothing to note.

<br>

### Carbon System<br>

  ##### Methodology<br>
  Carbon system measurements are performed by the Wang lab (Woods Hole Oceanographic
  Institution). DIC and TA measurements follow the methodology of Wang and Cai (2004)
  with uncertainties of 2 umol/kg. DIC measurements are performed with an Apollo
  Sci-Tech AS-C3. TA measurements are performed with an Apollo Sci-Tech AS-ALK2
  and ROSS electrode. pH measurements follow the methodology of Clayton and Byrne
  (1993) with an uncertainty of 0.002 pH units using an Agilent 8453.<br>

  ##### Notes<br>
  Nothing to note.

### Chlorophyll and Phaeo<br>
  ##### Methodology<br>
  Analysis was completed using a Turner Designs Aquafluor Handheld 800446


  ##### Notes<br>
  | Station-Cast #  | Bottle Position | Comment |
  | --------------- | --------------- | ------- |
  | 4 | 7 | Pick hair off filter |
  | 4 | 8 | Pick copepod off filter |
  | 6 | 5 | extreme phaeo:chl ratio but extremely deep sample so reasonable and in noise of fluorometer |


<br>

---
### Data Flag Description
  The data flags are presented in the summary sheet as a 16-bit array, read from
  right-to-left, where a 1 in a particular bit position indicates a particular
  flag meaning applies. For example, a flag of 0000000000000010 for the column
  **CTD File Flag** indicates that the cast was a data cast only.

  Additionally, these data flags an assessment of the collection and processing
  of the relevant data or samples, and are not an assessment of the *accuracy*
  of the data. For example, a conductivity sensor which has the correct
  calibration coefficients and functions normally will receive a quality flag of
  0000000000000100 (acceptable measurement). However, the calibration
  coefficients may be out of date and off with respect to the discrete salinity
  results; this does not affect the assigned flag.

| Bit Position | Cast Flag                                              | CTD File Flag                                     | CTD Parameter Flag                               | Niskin Flag                      | Discrete Sample Flag                                                | Discrete Replicate Flag              |
| ------------ | ------------------------------------------------------ | ------------------------------------------------- | ------------------------------------------------ | -------------------------------- | ------------------------------------------------------------------- | ------------------------------------ |
| 0            | Notes/Other                                            | Notes/Other                                       | Notes/Other                                      | Notes/Other                      | Notes/Other                                                         | Notes/Other                          |
| 1            | Delayed start to data collection                       | Data cast only                                    | Not Calibrated                                   | Bottle information unavailable   | Sample for this measurement was drawn but analysis not yet received | Duplicate analysis on same Sample    |
| 2            | Acceptable; normal cast according to SOP               | Acceptable; file processed according to SOP       | Acceptable measurement                           | No problems noted                | Acceptable; sample processed according to SOP                       | Single Sample                        |
| 3            | Non-standard winch speed                               | File processed using modified parameters          | Questionable measurement                         | Leaking                          | Questionable measurement                                            | Duplicate analysis from same Niskin  |
| 4            | Non-standard surface soak time                         | File processed using alternate XMLCON             | Bad measurement                                  | Ran out of water during sampling | Bad measurement                                                     | Triplicate analysis from same Niskin |
| 5            | Non-standard bottle soak time                          | Missing scans as indicated by module error counts | Not reported                                     | Vent open                        | Not reported                                                        | Unassigned                           |
| 6            | Sensor issues but cast completed and data collected    | Missing metadata                                  | Calibration coefficients greater than 1 year old | Misfire at wrong depth           | Sample collected out-of-order                                       | Unassigned                           |
| 7            | Cable issues but cast completed and data collected     | Unassigned                                        | Corresponding discrete sample                    | Unknown problem                  | Sample processed using alternative methods; see notes               | Averaged value from replicate samples|
| 8            | Winch issues but cast completed and data collected     | Unassigned                                        | Unassigned                                       | Unassigned                       | Unassigned                                                          | Unassigned                           |
| 9            | Premature cast end with data and/or data loss          | Unassigned                                        | Unassigned                                       | Unassigned                       | Sample not drawn for this measurement from this bottle              | Unassigned                           |
| 10           | Significant ship heave                                 | Unassigned                                        | Unassigned                                       | Unassigned                       | Unassigned                                                          | Unassigned                           |
| 11           | Station position not adequately maintained during cast | Unassigned                                        | Unassigned                                       | Unassigned                       | Unassigned                                                          | Unassigned                           |
| 12           | Tow-yo, Yo-yo cast                                     | Unassigned                                        | Unassigned                                       | Unassigned                       | Unassigned                                                          | Unassigned                           |
| 13           | ROV Bottle sample                                      | Unassigned                                        | Unassigned                                       | Unassigned                       | Unassigned                                                          | Unassigned                           |
| 14           | Unassigned                                             | Unassigned                                        | Unassigned                                       | Unassigned                       | Unassigned                                                          | Unassigned                           |
| 15           | Unassigned                                             | Unassigned                                        | Unassigned                                       | Unassigned                       | Unassigned                                                          | Unassigned                           |
