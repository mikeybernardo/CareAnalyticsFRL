# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 13:57:40 2018

@author: RieneckerS
"""
## Script reads XML file from CareAnalytics, calculates CTDI and DLP values for each protocol and saves to Excel table
from xml.dom import minidom # Import minidom for reading XML files
import numpy as np #Import Numpy for working with arrays

from pandas import DataFrame

#Parse XML file by name
mydoc = minidom.parse(r'')
doseinfo = mydoc.getElementsByTagName('DoseInfo')

# Parse XML Data
study = []
ages = []
date = []

for elem in doseinfo:
    study.append(elem.attributes['StudyDescription'].value)
    ages.append(elem.attributes['PatientsAge'].value)
    date.append(elem.attributes['StudyDate'].value)


patient_num = len(doseinfo) # Number of Patients
study = np.array(study) #  Study Descriptions array
date = np.array(date).astype(int) # Dates array
start_date = min(date) 
end_date = max(date)

ages = [word.replace('Y','') for word in ages] # Sort Ages
ages = [word.replace('0','') for word in ages]
ages = np.array(ages).astype(int)  

# Sort CT Acquisition Data
acq_protocol = []
ctdi_vol = []
dlp = []

cNodes = mydoc.childNodes
#nList = cNodes[0].getElementsByTagName("DoseInfo")
for node in cNodes:
    eList = node.getElementsByTagName("CT_Acquisition")
    for elem in eList:
        acq_protocol.append(elem.attributes['Acquisition_Protocol'].value) # Get Acquisition Protocols
    for elem in eList:
        ctdi_vol.append(elem.attributes['Mean_CTDIvol'].value) # Get CTDI 
    for elem in eList:
        dlp.append(elem.attributes['DLP'].value) # Get DLP
        
protocol_unique = set(acq_protocol); # Find unique acquisition protocols
protocols = sorted(list(protocol_unique)); # Sort acquisition protocols alphabetically

# Convert List of Values to Array of Numbers or Strings        
acq_protocol = np.array(acq_protocol)
ctdi_vol = [word.replace(' mGy','') for word in ctdi_vol] # Remove units from string
ctdi_vol= np.array(ctdi_vol).astype(float) # Convert list of strings to array of floating numbers
dlp = np.array(dlp).astype(float) # Convert DLP values to floating numbers

# Calculate CTDI and DLP values for each acquisition protocol
count_number = []
ctdi_min = []
ctdi_max = []
ctdi_25 = []
ctdi_50 = []
ctdi_75 = []
dlp_min = []
dlp_25 = []
dlp_50 = []
dlp_75 = []
dlp_max = []

for i in range(0, len(protocols)):
    acq_selection = np.where(acq_protocol==protocols[i])[0]
    all_ctdi = ctdi_vol[acq_selection] # Select CTDI values
    all_dlp = dlp[acq_selection] # Select DLP Values#
    
    count_number.append(len(all_dlp)); # Count number of scans for each protocol
    
    ctdi_min.append(np.min(all_ctdi));
    ctdi_25.append(np.percentile(all_ctdi,25));
    ctdi_50.append(np.percentile(all_ctdi,50)); # Median CTDI value
    ctdi_75.append(np.percentile(all_ctdi,75));
    ctdi_max.append(np.max(all_ctdi));

    dlp_min.append(np.min(all_dlp))
    dlp_25.append(np.percentile(all_dlp,25))
    dlp_50.append(np.percentile(all_dlp,50)) # Median DLP value
    dlp_75.append(np.percentile(all_dlp,75))
    dlp_max.append(np.max(all_dlp))

# Display Data in Table    
FRL_report = DataFrame({ 'Acquisition Protocol': protocols, 'Scans': count_number,'DLP Min' : dlp_min,'DLP 25%' : dlp_25, 'DLP 50%' : dlp_50,'DLP 75%' : dlp_75, 'DLP Max' : dlp_max,
                        'CTDI Min': ctdi_min, 'CTDI 25%' : ctdi_25, 'CTDI 50%' : ctdi_50,'CTDI 75%' : ctdi_75, 'CTDI Max': ctdi_max}) 
    
FRL_report = FRL_report[['Acquisition Protocol','Scans','CTDI Min','CTDI 25%','CTDI 50%','CTDI 75%','CTDI Max',
                        'DLP Min','DLP 25%','DLP 50%','DLP 75%','DLP Max']]

# Save Table to Excel
#user_filename = input('Save FRL report to the following file name: ') # Get File Name from user
#FRL_report.to_excel(user_filename, sheet_name='sheet1', index=False)

#del user_filename, FRL_report

#FRL_report.to_csv(user_filename) # Save File in .csv format
