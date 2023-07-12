#!/usr/bin/env python

import sys
import os
import re
# import numpy as np
import argparse

#command line options
parser = argparse.ArgumentParser()
parser.add_argument("--subjects",help="process listed subjects",nargs='+',action="store",required=True)
args = parser.parse_args()

#set paths
subjects = args.subjects
logfiledir = "/Users/jonask/fMRI/SAGE/logfiles"
outputfolder = "/Users/jonask/fMRI/SAGE/fslstimfiles"
allfiles = os.listdir(logfiledir)

#filter logfiles for desired subjects
logfiles = []
for subject in subjects:
	logfiles += [elem for elem in allfiles if subject in elem and ".txt" in elem]

print("Will process these logfiles:")
print(logfiles)

pattern = "^\d\d.*"

#parse each logfile
for logfile in logfiles:

	basename = os.path.splitext(logfile)[0]
	outfile = "%s/%s_fsl.txt" % (outputfolder,basename)
	print("outputfile is %s" % outfile)

	logfilepath = "%s/%s" % (logfiledir,logfile)
	logfilehandle = open(logfilepath)
	lines = [elem for elem in logfilehandle.readlines() if "#" not in elem]

	run = 0 

	for line in lines:
		result = re.match(pattern,line)
		if (result):
			(trial, stim, cond, lag, lbin, startt, resp, corr, rt) = line.split(",")
			
			trial = int(trial)
			startt = float(startt)
			run = (trial // 81) + 1

			print("Run %d: Trial %d at %.3f" % (run,trial,startt) )

			stimfilename = "%s/%s_run%d_%s.txt" % (outputfolder,subject,run,cond)
			stimfile = open(stimfilename,"a")
			stimfile.write("%.2f %.2f 1\n" % (startt,float(rt)))
			stimfile.close()