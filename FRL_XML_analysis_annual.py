# -*- coding: utf-8 -*-
"""
Created on Wed May  9 15:54:30 2018

@author: RieneckerS
"""

## Script reads XML file from CareAnalytics, calculates CTDI and DLP values for each protocol and saves to Excel table
from xml.dom import minidom # Import minidom for reading XML files
import numpy as np #Import Numpy for working with arrays
from pandas import DataFrame
import os
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

rad_logs = []

# Find all files in the directory for a certain scanner
for file in os.listdir(r'\\qldhealth\\.NBR-CL1_DATA3.Nambour.SCG.BNN.HEALTH\\MedImage\\BTS\\MedPhys Projects\\FRL for CTs\\Radiation Dose Logs\\'):
    if file.startswith('Force75568'):
        rad_logs.append(os.path.join(r'\\qldhealth\\.NBR-CL1_DATA3.Nambour.SCG.BNN.HEALTH\\MedImage\\BTS\\MedPhys Projects\\FRL for CTs\\Radiation Dose Logs\\', file))

# Get Data from XML files
mydoc = []
doseinfo = []
#study = []
#ages = []
date = []
acq_protocol = []
ctdi_vol = []
dlp = []

cNodes = []
eList = []

for i in range(0,len(rad_logs)):
    mydoc.append(minidom.parse(rad_logs[i]))
    doseinfo.append(mydoc[i].getElementsByTagName('DoseInfo'))
    
    for elem in doseinfo[i]:
        #study.append(elem.attributes['StudyDescription'].value)
        #ages.append(elem.attributes['PatientsAge'].value)
        date.append(elem.attributes['StudyDate'].value)
    
    cNodes.append(mydoc[i].childNodes)
    #nList.append(cNodes[0].getElementsByTagName('DoseInfo'))
    
    for node in cNodes[i]:
        eList.append(node.getElementsByTagName("CT_Acquisition"))
    for elem in eList[i]:
            acq_protocol.append(elem.attributes['Acquisition_Protocol'].value)
    for elem in eList[i]:
        ctdi_vol.append(elem.attributes['Mean_CTDIvol'].value) # Get CTDI 
    for elem in eList[i]:
        dlp.append(elem.attributes['DLP'].value) # Get DLP

del rad_logs, cNodes, eList, file, mydoc, doseinfo
# Analyse Data from Unique Acquisition Protocols        
protocol_unique = set(acq_protocol); # Find unique acquisition protocols
protocols = sorted(list(protocol_unique)); # Sort acquisition protocols alphabetically

# Convert List of Values to Array of Numbers or Strings        
acq_protocol = np.array(acq_protocol)
ctdi_vol = [word.replace(' mGy','') for word in ctdi_vol] # Remove units from string
ctdi_vol= np.array(ctdi_vol).astype(float) # Convert list of strings to array of floating numbers
#dlp = [word.replace(' mGycm','') for word in dlp] # Remove units from string for DefinitionFH_NGH
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
ctdi_p = []
dlp_p = []

for i in range(0, len(protocols)):
    acq_selection = np.where(acq_protocol==protocols[i])[0] # All instances of the selected protocol
    all_ctdi = ctdi_vol[acq_selection] # Select CTDI values
    all_dlp = dlp[acq_selection] # Select DLP Values
    
    ctdi_p.append(ctdi_vol[acq_selection]);
    dlp_p.append(dlp[acq_selection]);
    
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

del acq_protocol, ctdi_vol, dlp, acq_selection, i, all_ctdi, all_dlp

# Get Date Range
date = np.array(date).astype(int) # Dates array
start_date = min(date) 
end_date = max(date)    

# Display Data in Table    
FRL_report = DataFrame({ 'Acquisition Protocol': protocols, 'Scans': count_number,'DLP Min' : dlp_min,'DLP 25%' : dlp_25, 'DLP 50%' : dlp_50,'DLP 75%' : dlp_75, 'DLP Max' : dlp_max,
                        'CTDI Min': ctdi_min, 'CTDI 25%' : ctdi_25, 'CTDI 50%' : ctdi_50,'CTDI 75%' : ctdi_75, 'CTDI Max': ctdi_max, 'Start Date' : start_date, 'End Date' : end_date}) 
    

#del protocols, count_number, dlp_min, dlp_25,  dlp_50, dlp_75, dlp_max, ctdi_min, ctdi_25, ctdi_50, ctdi_75, ctdi_max, start_date, end_date, date

FRL_report = FRL_report[['Acquisition Protocol','Scans','CTDI Min','CTDI 25%','CTDI 50%','CTDI 75%','CTDI Max',
                        'DLP Min','DLP 25%','DLP 50%','DLP 75%','DLP Max', 'Start Date', 'End Date']]

# Save Table to Excel
#user_filename = input('Save FRL report to the following file name: ') # Get File Name from user
#FRL_report.to_excel(user_filename, sheet_name='sheet1', index=False)

#FRL_report.to_csv(user_filename) # Save File in .csv format
