#import packages
import re
import pandas as pd


#IMPORT FILES
#while loop to prevent program cracking
success = False                                    
while not success:
	filename = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
	filepath = filename + ".txt"
	
	#open file check
	try:
		file = open(filepath, "r")
		print("Successfully opened {}".format(filepath))
		success = True
	except:
		print("File cannot be found")



#ANALYZING
print(" \n**** ANALYZING ****")

#init vars
tot_line = 0
tot_invalid = 0
records = []                                  #record for all VALID participants

#check error and grade by looping over each participant's record
lines = file.readlines()

for line in lines:
	#data cleaning
	line = line.strip()                          #strip /n, /t, and whitespace
	tot_line += 1
	list_line = line.split(",")                  #convert into list
	
	#number of values not match 26 (INVALID RECORD)
	if len(list_line) != 26:
		print("Invalid line of data: does not contain exactly 26 values:")
		print(line)
		tot_invalid += 1

	#ID error (INVALID RECORD)
	elif not re.match(r"^N\d{8}" ,list_line[0]):
		print("Invalid line of data: N# invalid")
		print(line)
		tot_invalid += 1

	#grading process (ONLY FOR VALID RECORD)
	else:
		answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
		answer_list = answer_key.split(",")          #convert into list
		grade = [list_line[0]]                       #record for 1 VALID participant

		#loop comparing answer of participants vs answer_key
		for i in range(len(answer_list)):
			#correct answer
			if list_line[i+1] == answer_list[i]:
				grade.append(4)
			#empty_answer
			elif list_line[i+1] == "":
				grade.append(0)
			#wrong answer
			else:
				grade.append(-1)

		#calculate sum of each participant + importing individual record into overal records
		grade.append(sum(grade[1:27]))
		records.append(grade)
				
#no error
if tot_invalid == 0:
	print("No errors found!")


#SUMMARIZE
print(" \n**** REPORT ****")

#convert to pd.DataFrame
pd_records = pd.DataFrame(records)

#output
#lines_summary
print("Total lines of data:",           tot_line)
print("Total valid lines of data:",     tot_line - tot_invalid)
print("Total invalid lines of data:",   tot_invalid)

#students_summary
print("Total students of high scores:", pd_records[pd_records[26]>=80].shape[0])
print("Mean (average) score:",          round(pd_records.iloc[:,26].mean(),3))
print("Highest Score:",                 pd_records.iloc[:,26].max())
print("Lowest score:",                  pd_records.iloc[:,26].min())
print("Range of scores",                pd_records.iloc[:,26].max() - pd_records.iloc[:,26].min() )
print("Median score:",                  pd_records.iloc[:,26].median())

#questions summary
#skipped question
skipped_question = []
string1 = ""                       #output

#loop though 25 questions
for i in range(1,26):
	skipped_question.append(pd_records[pd_records.iloc[:,i] == 0].shape[0])

#convert to pd.Series
pd_skipped_question = pd.Series(skipped_question)

#max_skipped_question + ratio 
max_skipped_question = pd_skipped_question.max()
ratio = round(max_skipped_question/(tot_line - tot_invalid), 3)

#tracing questions that has similiar number of skips
for i in range(25):
	if skipped_question[i] == max_skipped_question:
		string1 += "{} - {} - {}, ".format(i+1, max_skipped_question, ratio) 

#output
print("Question that most people skip:", string1)

#incorrect question
#skipped question
incorrect_question = []
string2 = ""                           #output

#loop though 25 questions
for i in range(1,26):
	incorrect_question.append(pd_records[pd_records.iloc[:,i] == -1].shape[0])

#convert to pd.Series
pd_incorrect_question = pd.Series(incorrect_question)

max_incorrect_question = pd_incorrect_question.max()
ratio = round(max_incorrect_question/(tot_line - tot_invalid), 3)

#loop to find similiar incorrect questions that has same num of incorrections
for i in range(25):
	if incorrect_question[i] == max_incorrect_question:
		string2 += "{} - {} - {}, ".format(i+1, max_incorrect_question, ratio)

#output
print("Question that most people answer incorrectly:", string2)


#FILE SAVE
ovl_record = pd_records.iloc[:,[0,26]]
ovl_record.to_csv('{}_grades'.format(filename))