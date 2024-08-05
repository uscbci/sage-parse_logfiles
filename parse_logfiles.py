#!/usr/bin/env python

import sys
import os
import re

# set paths
logfiledir = "/Volumes/BCI/SAGE/logfiles"
outputfolder = "/Volumes/BCI/SAGE/fslstimfiles"

# We will process all files that haven't already been processed
allfiles = os.listdir(logfiledir)
donefiles = os.listdir(outputfolder)
logfiles = [elem for elem in allfiles if elem[4:9] not in donefiles ]

print("Will process these logfiles:")
print(logfiles)

pattern = "^\d.*"

# parse each logfile
for logfile in logfiles:

	subject = logfile[4:9]
	outputfolder = outputfolder + "/" + subject
	if ( not os.path.exists(outputfolder)):
		os.mkdir(outputfolder)

	basename = os.path.splitext(logfile)[0]
	outfile = "%s/%s_fsl.txt" % (outputfolder,basename)
	print("outputfile is %s" % outfile)

	logfilepath = "%s/%s" % (logfiledir,logfile)
	logfilehandle = open(logfilepath)
	lines = [elem for elem in logfilehandle.readlines() if "#" not in elem]

	run = 0

	trialcounter = {"new":0, "old_correct": 0, "old_similarerror": 0, "old_newerror" : 0, "similar_correct": 0, "similar_olderror": 0, "similar_newerror": 0, "junk" :0}

	for line in lines:
		result = re.match(pattern,line)
		if (result):
			items = line.split(",")
			#(trial, stim, cond, lag, lbin, startt, resp, corr, rt) = line.split(",")
			
			condition = ""

			trial = int(items[0])
			startt = float(items[5])

			if (len(items) > 7):
				rt = items[6]
				cond = int(items[2])
				resp = int(items[6]) 
				corr = int(items[7])
				if (cond == 0 or cond == 2):
					condition = "new"
				if (cond == 1 and corr == 1):
					condition = "old_correct"
				if (cond == 1 and corr == 0):
					if (resp == 2 ):
						condition = "old_similarerror"
					if (resp == 3):
						condition = "old_newerror"
				if (cond == 3 and corr == 1):
					condition = "similar_correct"
				if (cond == 3 and corr == 0):
					if (resp == 1):
						condition = "similar_olderror"
					if (resp == 3):
						condition = "similar_newerror"
			else:
				condition = "junk"

			if (trial >=0 and trial <= 80):
				run = 1
			if (trial > 80 and trial <= 160):
				run = 2
			if (trial > 160 and trial <= 240):
				run = 3
			if (trial > 240):
				run = 4

			trialcounter[condition] = trialcounter[condition] + 1


			print("Run %d: Trial %d at %.3f %s" % (run,trial,startt, condition) )

			stimfilename = "%s/%s_run%d_%s_all.txt" % (outputfolder,subject,run,condition)
			stimfile = open(stimfilename,"a")
			stimfile.write("%.2f 3.5 1\n" % (startt))
			stimfile.close()

			stimfiletrial_name = "%s/%s_run%d_%s_%d.txt" % (outputfolder,subject,run,condition,trialcounter[condition])
			stimfiletrial = open(stimfiletrial_name,"a")
			stimfiletrial.write("%.2f 3.5 1\n" % (startt))
			stimfiletrial.close()