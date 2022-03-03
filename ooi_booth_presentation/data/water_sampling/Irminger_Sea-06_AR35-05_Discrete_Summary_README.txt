# Irminger_Sea-06_AR35-05
---
Author: Andrew Reed <br>
Date: 2021-09-13 <br>
Version: 1-02 <br>
Updates: Added DIC, TA, pH data from lab.

---
Author: Andrew Reed <br>
Date: 2021-05-17 <br>
Version: 1-01 <br>
Updates: Fixed column header spellings. Checked format of spreadsheet.

---
Author: Andrew Reed <br>
Date: 2021-01-21 <br>
Version: 1-00 <br>
Notes: Optimized for Markdown

---
### File Processing<br>
  ##### Methodology
There should be one row for each station-cast-niskin bottle. Multiple samples for the same
parameter from a single niskin bottle are split into separate rows, with the associated
CTD data copied to the new row. The first row of the file is the column headers. <br>

  ##### Notes<br>
  The pylon on the CTD rosette failed at the start of the cruise. Consequently, some Niskin
  bottles were collected by using acoustic release. Water depths, pressures, and times for
  bottles collected by acoustic release should be taken as approximate. <br>

  | Station-Cast #  | Bottle Position | Comment |
  | --------------- | --------------- | ------- |
  | 1 | All | Acoustic release test cast; no data for upcast |
  | 2 | All | No samples due to pylon failure |
  | 3 | All | No samples due to pylon failure; OOI DOSTA on rosette |
  | 4 | All | No samples due to pylon failure; OOI DOSTA on rosette |
  | 5 | All | No samples due to pylon failure; OOI DOSTA on rosette |
  | 6 | All | No samples due to pylon failure; OOI DOSTA on rosette |
  | 7 | All | Cast for SSV profile for CASIUS |
  | 8 | 7, 11, 19 | 3 bottles fired by acoustic releases; OOI DOSTA on rosette; primary conductivity, temperature and oxygen are suspect below ~500 m |
  | 9 | 7, 8, 11, 12, 19, 20, 23, 24 | 8 bottles fired at 4 depths by acoustic releases, OOI DOSTA on rosette; primary conductivity, temperature and oxygen are suspect |
  | 10 | 7, 8, 11, 12, 19, 20, 23, 24 | 8 bottles fired at 4 depths by acoustic releases, OOI DOSTA on rosette; primary conductivity, temperature spike at ~1400 m; oxygen is suspect |
  | 11 | 1 - 24 | OOI DOSTA on rosette; primary conductivity, temperature and oxygen are suspect |
  | 11 | 8, 10, 12, 15 | Non-OOI sample stops |
  | 12 | 1 - 15 | OOI DOSTA on rosette; primary conductivity spike at ~2300 m; oxygen is suspect |
  | 12 | 13 - 15 | Non-OOI sample stops |
  | 13 | 1 - 22 | OOI DOSTA on rosette; oxygen is suspect; oxygen not connected to plumbing |
  | 13 | 2 | Bottle may have closed at wrong depth |
  | 13 | 6, 8, 10, 12, 14, 16, 18, 20, 21, 22 | Non-OOI sample stops |


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
  Samples still being processed.


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
