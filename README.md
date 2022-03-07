# Ocean Sciences 2022
Author: Andrew Reed

---
## Overview
Welcome. This repo contains the notebooks necessary to recreate the analyses from my Ocean Sciences 2022 talks, as well my walkthrough of OOI Bottle Data processing from the OOI Booth talks:
1. **QARTOD in Practice: Two Examples from the Ocean Observatories Initative**
2. **OOI Carbon System: Data Validation for the Irminger Sea Array**
3. **Preparing OOI discrete bottle data for comparison with OOI pCO2 and pH timeseries data**

Additonally, this repo contains the presentations themselves as well as the necessary input data and metadata when needed.

## Setup

0. **Make an account on OOINet**
First, please go to https://ooinet.oceanobservatories.org/ and make an register. Once you have made an account for yourself and logged in, navigate to your account settings by clicking on "User Profile" under your email in the top right corner of your screen. Once at your Profile, record your API Username and API Token. These are necessary if you wish to access and download data from the Ocean Observatories API.

1. **Setup python environment**
Its recommended that miniconda or anaconda3 has been installed. The python environment can be setup with the following commands:

    ```
    conda env create -f environment.yaml
    ```

2. **Launch jupyter notebooks**
Now you are ready to get working with OOI data! Launch a jupyter notebook in your browser and get ready to explore OOI carbon system data.

---
### Project Files Description
---
#### Dependencies
The example notebooks in this repo rely heavily on packages, functions, and routines that have been developed over the years by the OOI operators to assist in processing and working with OOI data. There are two principle repos on which the example notebooks lean are:

* ##### OOINet
> The modules and tools within this repo are designed to assist in requesting, importing, downloading, and vizualizing data from the Ocean Observatories Initiative API by M2M requests. It can be found at https://github.com/reedan88/OOINet.

* ##### OOI-Data-Explorations
> Explorations of Ocean Observatories Initiative Datasets via MATLAB, Python, R, and Julia. It can be found at https://github.com/oceanobservatories/ooi-data-explorations.

These repos are not distributed on either conda or pip, so they will need to be either cloned to your local machine or the files and functions directly downloaded.

Additionally, specific functions written to simplify and streamline the analyses in this repo are stored as modules within the OS2022 subdirectory in this repo.

#### carbon_system
##### Notebooks
* **Identify_and_Download_Data.ipynb** - The purpose of this notebook is to identify and download the datasets with pH and pCO2 data deployed at the Ocean Observatory Initiative's (OOI) Global Irminger Array (60$^{\circ}$N, 39$^{\circ}$W). OOI deploys the following sensors for measuring the ocean carbon system: Sunburst Sensors, LLC. SAMI-pH (PHSEN) pH, SAMI-pCO$_{2}$ seawater measurements, and the Pro-Oceanus pCO2 sensor measurements. The datasets identified here are used in the **```Data_Analysis```** notebook.
* **Bottle_Data.ipynb** - This notebook provides a quick outline and example of working with OOI Discrete Summary Spreadsheet bottle data. It includes how to load it, how to parse data quality flags, how to derive some important values, and work with the data to make it easy to use for data validation and comparison purposes.
* **Data_Analysis.ipynb** - The purpose of this notebook is to analyze and validate the performance of the Sunburst Sensors, LLC. SAMI-pH (PHSEN) pH, SAMI-pCO$_{2}$ seawater measurements, and the Pro-Oceanus pCO2 sensor measurements at the Global Irminger Array. This is done on a deployment-by-deployment, site-by-site comparison with the pH measurements from discete water samples collected by Niskin Bottle casts during deployment and recovery of the instrumentation during mooring maintainence.

#### event_detection
##### Notebooks
* **Argentine_Basin.ipynb** - This notebook assess how well the QARTOD climatology test, as implemented by OOI, performs with respect to accurately capturing and flagging the passage of a mid-water-column eddy across the OOI Global Argentine Basin array in July-August of 2016.
* **Irminger.ipynb** - This notebook assess how well the QARTOD gross range test, as implemented by OOI, performs with respect to accurately flagging practical salinity data from the mid-water-column in the Irminger Sea with respect to a long-term freshening signal.

#### Files in this repo
* **utils.py**
* **bottle_utils.py**
* **environment.yaml**

#### Files outside this repo
* **user_info.yaml** - a YAML file which has the user's OOI API username and token. This is not available in the repo; the user should make one for themselves, and place it in the parent directory of their copy of this repo) _This file is specifically excluded in the .gitignore._
