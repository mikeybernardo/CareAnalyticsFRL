#
# This script runs CareAnalytics (CA) from the command line on connected systems
# and outputs the XML files to a designated folder for analysis.

__author__ = 'Mikey Bernardo'

import subprocess
import shutil
import os
import time

print("Running program...")

# Load CA directory
os.chdir("C:\CareAnalytics\CareAnalytics_Ver2")

# Run CAtool on connected nodes
DefEdge = 'CAtool.exe /sr ct /node DefinitionEdge /w 01 /out DefEdge.xml'
Force75568 = 'CAtool.exe /sr ct /node Force75568 /w 01 /out Force75568.xml'
Force75566 = 'CAtool.exe /sr ct /node Force75566 /w 01 /out Force75566.xml'
Force75564 = 'CAtool.exe /sr ct /node Force75564 /w 01 /out Force75564.xml'
ArtisZeeMP = 'CAtool.exe /sr Xray /node ArtisZeeMP /w 01 /out ArtisZeeMP.xml'
ArtisZeegoQ = 'CAtool.exe /sr Xray /node ArtisZeegoQ /w 01 /out ArtisZeegoQ.xml'
Symbia2078 = 'CAtool.exe /sr ct /node Symbia2078 /w 01 /out Symbia2078.xml'
Symbia2079 = 'CAtool.exe /sr ct /node Symbia2079 /w 01 /out Symbia2079.xml'
BiographMCT = 'CAtool.exe /sr ct /node BiographMCT /w 01 /out BiographMCT.xml'
DefinitionFH_NGH = 'CAtool.exe /sr ct /node DefinitionFH_NGH /w 01 /out DefinitionFH_NGH.xml'

systems = [DefEdge, Force75568, Force75566, Force75564, ArtisZeeMP, ArtisZeegoQ, Symbia2078, Symbia2079, BiographMCT, DefinitionFH_NGH]
nodes = ["DefEdge", "Force75568", "Force75566", "Force75564", "ArtisZeeMP", "ArtisZeegoQ", "Symbia2078", "Symbia2079", "BiographMCT", "DefinitionFH_NGH"]

# Final destination folder for storing the XML files
DestFolder = "\\\QLDHEALTH\.NBR-CL1_DATA3.Nambour.SCG.BNN.HEALTH\MedImage\BTS\MedPhys Projects\FRL for CTs\Radiation Dose Logs"

# Create XML files using CAtool
for i in systems:
    subprocess.run(i)
    print(i)

print("Output of SR into generic files has finished.")

# Rename and move XML files onto server
for i in nodes:
    os.rename(i + ".xml", i + time.strftime("_%Y_%m_%d.xml"))
    shutil.move(i + time.strftime("_%Y_%m_%d.xml"), str(DestFolder))
    print("Renaming and moving " + i + " file to server has completed.")

print("Program finished. Have a nice day!")