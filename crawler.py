import requests
import pprint
from bs4 import BeautifulSoup
import json
import re

# this files crawles our 7th semester result.




# r = requests.post("http://bcsociety.org/nit/index.php?Link=Result Details", data={'class':'IT','Semester':'7','Batch': '2012','hi':'abcdaa455hkfg','rollno':'552'})
# pprint.pprint(r.content)

# data={'item':'abcdaa455hkfg','Link':'Result Search'},

# pprint.pprint(t.content)

POINTER = {'NA':-1,'F': 0, 'C': 5, 'C+': 6, 'B': 7, 'B+': 8, 'A': 9, 'A+': 10}



input_file_name = 'CS_students.json'
openFile =  open(input_file_name, 'r')
inputFile = json.load(openFile)

students = inputFile['students']
subjects = inputFile['subjects']

total_students = len(students)
toal_subjects = len(subjects)
print "%d students found." % total_students
print "%d subjects." % toal_subjects
student_count = 1

# students = students[3:1]
# subjects = subjects[7:]

student_results = []
subject_wise_results = {}
# students_processed = []


for subject in subjects:
	subject_wise_results[str(subject['subject'])] = []


for student in students:
	rollno = int(student['rollno'])
	name = str(student['name'])
	print "[%d][%d] Querying for %s" % (total_students-student_count,student_count,name)
	# student_results.setdefault(student["rollno"],[])

	student_result = {}
	student_result['rollno'] = rollno
	student_result['name'] = name

	grades = []
	for subject in subjects:
		subject_name = str(subject['subject'])
		print "Querying for %s" % (subject_name)
		t = requests.post("http://bcsociety.org/nit/" + subject['url'], data={'rollno': rollno})
		soup = BeautifulSoup(t.content, 'html.parser')
		bogie = soup.find_all('td')
		grade_obtained = 'NA'
		# print bogie

		if len(bogie):
			grade_obtained = str( bogie[len(bogie)-1].string)
			# another hacky attempt
			if (not grade_obtained) or grade_obtained == 'None' or grade_obtained == ' ':
				grade_obtained = str(soup.find_all('td', text=re.compile('grade|GRADE|Grade'))[0].next_sibling.string)
				# print grade_obtained

			if (not grade_obtained) or grade_obtained == 'None' or grade_obtained == ' ':
				grade_obtained = 'NA'

		# print {'grade':grade_obtained,'sub': subject_name, 'pointer' : POINTER[grade_obtained] }
		grades.append({'grade':grade_obtained,'sub': subject_name, 'pointer' : POINTER[grade_obtained]})
		subject_wise_results[subject_name].append({'rollno': rollno, 'grade': grade_obtained, 'pointer' : POINTER[grade_obtained], 'name' : name })
		# {'rollno': rollno, 'grade': grade_obtained, 'pointer' : POINTER[grade_obtained], 'name' : name }
	student_result['grades'] = grades
	student_results.append(student_result)
	student_count+= 1

# pprint.pprint(student_results)
# pprint.pprint(subject_wise_results)

data = {}
data['student_wise_results'] = student_results
data['subject_wise_results'] = subject_wise_results

with open(input_file_name.replace(".json",'_result.json'), 'w') as outfile:
    json.dump(data, outfile)

print "all student's data processed"