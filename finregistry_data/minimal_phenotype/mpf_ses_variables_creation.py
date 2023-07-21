####################################################
#SOCIOECONOMIC VARIABLES FOR MINIMAL PHENOTYPE FILE#
####################################################

#First version created by Tuomo Hartonen on 22.03.2022

#The ouput file contains the following columns
#1. FinRegistryID
#2. SES - latest recorded socioeconomic status, sose column of the original file (SF socioeconomic), using only first digit of the code
#3. OCCUPATION - latest recorded occupation, first digit of the profession code (ammattikoodi), only 1995 classification or newer
#4. EDULEVEL - highest recorded level of education, first digit of the kaste_t2 column value, 1=education possibly ongoing
#5. EDUFIELD - field of education corresponding to the highest recorded level of education,
#first two digits of the iscifi2013 column, 11=education possibly ongoing

#Additional notes:

#Meaning of levels of the variable SES:
#1 = self-employed, agriculture
#2 = self-employed, non-agriculture
#3 = upper-level employees
#4 = lower-level employees
#5 = manual workers
#6 = students
#7 = pensioners
#8 = others
#9 = unknown/NA

#Meaning of levels of the variable OCCUPATION:
#0 = armed forces
#1 = managers
#2 = professionals
#3 = technicians and associate professionals
#4 = clerical and support workers
#5 = service and sales workers
#6 = skilled agricultural, forestry and fishery workers
#7 = craft and related trades workers
#8 = plant and machine operators, and assemblers
#9 = elementary occupations
#X = unknown occupation


#Note that the unique values for the highest degree are 3-8, although by definition we could have 0-9.
#Variable "education can still be ongoing" is set for each individual aged between 30 and 35.
#Education level variables have been created by taking the first digit of the column kaste_t2.
#Naming is based on:  https://www2.stat.fi/en/luokitukset/koulutusaste/koulutusaste_1_20160101/

#The field of education variables are derived by taking the first two digits of column iscifi2013 (these are ISCED 2013 codes).
#Individuas younger than 35 years old are treated so that their education can still be ongoing, meaning that for all of them we set EDULEVEL=1 and EDUFIELD=11.
#For each individual, the information from the latest entry is used, unless the newest education level is lower than a previous one.


#Meaning of levels of the variable EDULEVEL:
#0 = pre-primary education
#1 = education possibly ongoing
#2 = primary and lower secondary education
#3 = upper secondary education
#4 = specialist vocational education
#5 = short-cycle tertiary education
#6 = first-cycle higher education (e.g. Bachelor's)
#7 = second-cycle higher education (e.g. Master's)
#8 = third-cycle higher education (e.g. Doctor's)
#9 = level of education unknown or missing

#Meaning of levels of the variable EDUFIELD:
#00 = generic programmes and qualifications
#01 = education
#02 = arts and humanities
#03 = social sciences, journalism and information
#04 = business, administration and law
#05 = natural sciences, mathematics and statistics
#06 = information and communication technologies
#07 = engineering, manufacturing and construction
#08 = agriculture, forestry, fishery and veterinary
#09 = health and wellfare
#10 = services
#11 = possibly ongoing education (age<35)
#99 = field of education not found or unknown

#import needed libraries
from time import time
import csv

#define variables
outname = "/data/projects/mpf/mpf_create/mpf_ses_variables_22032022.csv"
header = ['FINREGISTRYID','SES','OCCUPATION','EDULEVEL','EDUFIELD']

#SOCIOECONOMIC STATUS
#--------------------

start = time()
#read in the socioeconomic status variables
sestatus_file = "/data/processed_data/sf_socioeconomic/sose_u1442_a.csv.finreg_IDsp"

ses_data = {} #key = FinRegistryID, value = [SES,OCCUPATION,EDULEVEL,EDUFIELD]

with open(sestatus_file,'rt') as infile:
	for row in infile:
		row = row.strip('\n').split(',')
		if row[0].count('FINREGISTRYID')>0: continue
		ID = row[0].strip('"')
		sose = row[3].strip('"')
		if len(sose)>0: sose = int(sose[0])
		else: sose = 9 #this means no sose code was found
		if ID not in ses_data: ses_data[ID] = [sose,'X','9','99']
		else:
			#this means we already have one status recorded, replacing it with the newer record, unless the newer is 9 (NA)
			if sose!=9: ses_data[ID][0] = sose

end = time()
print("Socioeconomic status variable created in "+str(end-start)+" s")

#OCCUPATION
#----------

start = time()
#read in the occupation variables
occupation_file = "/data/processed_data/sf_socioeconomic/ammatti_u1442_a.csv.finreg_IDsp"

with open(occupation_file,'rt',encoding='latin-1') as infile:
	for row in infile:
		row = row.strip('\n').split(',')
		ID = row[0].strip('""')
		if row[0].count('FINREGISTRYID'): continue
		code = row[3].strip('""')
		year = row[1].strip('""')
		if len(year)<1: year = 0
		else: year = int(float(year))
		if year<1995: continue #we use only the classification starting from 1995
		if len(code)<1: code = 'X' #missing values are coded as X=unknown/NA
		else: code = code[0]
		#only use the last occupation info for each inidividual
		if ID not in ses_data: ses_data[ID] = ['9',code,'9','99']
		elif code!='X': ses_data[ID][1] = code

end = time()
print("Occupation variable created in "+str(end-start)+" s")

#EDUCATION
#---------

start = time()
#read in the old minimal phenotype file to get the birth years of IDs. This is needed because people younger than 35 years old
#have been estimated to possibly still have their education ongoing

old_mpf_file = "/data/processed_data/minimal_phenotype/minimal_phenotype_2022-02-17.csv"
birth_years = {} #key=FINREGISTRYID, value=year of birth
with open(old_mpf_file,'rt') as infile:
	for row in infile:
		row = row.strip('\n').split(',')
		if row[0].strip('""')=='FINREGISTRYID': continue
		ID = row[0]
		birthyear = int(row[2].split('-')[0])
		birth_years[ID] = birthyear

#read in the education variables
education_file = "/data/processed_data/sf_socioeconomic/tutkinto_u1442_a.csv.finreg_IDsp"

with open(education_file,'rt',encoding='latin-1') as infile:
	for row in infile:
		row = row.strip('\n').split(',')
		if row[0].strip('""')=='FINREGISTRYID': continue
		ID = row[0].strip().strip('""')
		if ID not in ses_data: ses_data[ID] = ['9','X','9','99']
		if ID not in birth_years:
			#we decide to treat unknown birth years so that their education is still on going
			ses_data[ID][2] = '1'
			ses_data[ID][3] = '11'
		elif birth_years[ID]>1987:
			ses_data[ID][2] = '1'
			ses_data[ID][3] = '11' 
		else:    
			edu_field = row[3].strip().strip('"')[:2]
			if len(edu_field)<1: edu_field = '99'
			edu_level = row[4].strip().strip('""')[:1]
			if len(edu_level)<1: edu_level = '9' #99 marks NA
				
			if edu_level!='9':
				if (ses_data[ID][2]=='9') or (int(edu_level)>int(ses_data[ID][2])):
					#the newer entry is kept only if education level is higher than previously
					ses_data[ID][2] = edu_level
					ses_data[ID][3] = edu_field
end = time()
print("Education variables created in "+str(end-start)+" s")

start = time()
#now all variables have been initialized, save the resulting data to a file
with open(outname,'wt') as outfile:
	w = csv.writer(outfile,delimiter=',')
	w.writerow(header)
	for ID in ses_data: w.writerow([ID]+ses_data[ID])
end = time()
print("Output file written in "+str(end-start)+" s")
	
