# DistanceAndSchoolStats.py
# Rahul Murthy, 12/5/2015
# requires the requests library (http://docs.python-requests.org/en/latest/)
# place Spreadsheet named SchoolsAndAddresses2.csv in the same directory as this program
# SchoolsAndAddresses2.csv should contain in the columns: the name of the school, the school's address, city, zipcode
# run with python2.7 DistanceAndSchoolStats.py

# This program will first send a request to google maps (using a private api key) and recieve the driving distance in a .json format.
# Next this program will send a search request to the National Center for Education Statistics and retrieve and parse two pages to retrieve data about a school
# Finally all the data will be output into a file called distanceSpreadSheet2.csv in the format:
# name + ";" + address + ";" + city + ";" + zipcode + ";" + dist + ';' + titleOne + ';' + titleOneProgram + ';' + totalTeachers + ';' + totalStudents + ';' + ratio + ';' + freeLunch + ';' + reducedLunch + ';' + Private
# be sure to open this using semicolons as a column seperator




import requests
import json
from time import sleep



def main():

	# some variables
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7'}
	SchoolDataURL = ""
	searchterm = 'MoreInfo'
	recordsFound = "" 

	searchTerm_start_titleOne = 'Title I School:</font></strong>&nbsp;'
	searchTerm_end_titleOne = '<br />'
	titleOne = ''

	searchTerm_start_titleOneProgram = 'Title I School-Wide Program:</strong></font>&nbsp;'
	searchTerm_end_titleOneProgram = ';\n'
	titleOneProgram = ''

	searchTerm_local_totalTeachers = 'Teachers'
	searchTerm_start_totalTeachers = '<font size=\"3\">'
	searchTerm_end_totalTeachers = '</font></td>'
	totalTeachers = ''

	searchTerm_local_totalStudents = 'Total Students:'
	searchTerm_start_totalStudents = '<font size="3">'
	searchTerm_end_totalStudents = '</font></td>'
	totalStudents = ''

	searchTerm_local_ratio = 'Student/Teacher Ratio:'
	searchTerm_start_ratio = "<font size=\"3\">"
	searchTerm_end_ratio = '</font></td>'
	ratio = ''

	searchTerm_start_freeLunch = "Free lunch eligible: </strong></font>"
	searchTerm_end_freeLunch = "</td>"
	freeLunch = ""

	searchTerm_start_reducedLunch = 'Reduced-price lunch eligible: </strong></font>'
	searchTerm_end_reducedLunch = '</td>'
	reducedLunch = ""



	FoundSchool = False

	f = open('SchoolsAndAddresses2.csv', 'r')
	writeFileCSV = open('distanceSpreadSheet2.csv', 'w')


	for line in f:
		Private = ""
		test = line.decode('utf-8').strip()

		name,address,city,zipcode = test.split(';')

		skipAddress = False

		if not address: # if the address field is empty
			skipAddress = True
			
		addressFix = address.replace(" ", "+")
		addressFix = addressFix.replace("\'", "")
		addressFix = addressFix.replace("\n", "")

		nameFix = name.replace(" ", "+")
		nameFix = nameFix.replace("\'", "")
		nameFix = nameFix.replace("\n", "")
		nameFix2 = nameFix

		print (addressFix)
		addressFix = addressFix + "," + city + "," + zipcode

		cityfix = city.lower()

		schoolSearchString = 'http://nces.ed.gov/globallocator/index.asp?search=1&State=CA&city=' + cityfix + '&zipcode=&miles=&itemname=' + nameFix + '&sortby=name&School=1&PrivSchool=1'
		tempString = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + addressFix + '&destinations=1931+1st+Ave+Walnut+Creek&key=AIzaSyBhT_F8RWOu6Nb9zvr7UM_YkMbMlB_1mdA'
		
		# get the ad

		if skipAddress:
			dist = "??????"
		else:
			r = requests.request('Get', tempString)
			data = r.json()
			dist = data["rows"][0]["elements"][0]["distance"]["text"]


		output = name + " is " + dist + " away from lindsay"

		# now do the gov website


		t = requests.request('Get', schoolSearchString)
		tempFile = open('testfile.txt', 'w')

		tempFileObject = t.text.encode('utf-8')


		
		tempFile.write(tempFileObject)
		tempFile.close()
		tempFile = open('testfile.txt', 'r')

		

		

		for line in tempFile:
			templine = line.strip('&')
			if searchterm in line:
				print ("can get gov info!")
				FoundSchool = True
				startPos = line.find("ID=")
				endPos = line.find("\');\">", startPos)
				schoolIdNumber = line[startPos+3:endPos]
				privateTest = 'Private'
				if privateTest in line:
					SchoolDataURL = "http://nces.ed.gov/surveys/pss/privateschoolsearch/school_detail.asp?Search=1" + '&SchoolID=' + schoolIdNumber +  "&ID=" + schoolIdNumber
					Private = "Yes"
				else:
					SchoolDataURL = "http://nces.ed.gov/ccd/schoolsearch/school_detail.asp?Search=1" + '&SchoolID=' + schoolIdNumber +  "&ID=" + schoolIdNumber
					Private = "No"

		tempFile.close()

		if not FoundSchool: # try to remove words that are bad, like school, christian
			nameFix2 = nameFix2.replace("School", "")
			nameFix2 = nameFix2.replace("school", "")
			nameFix2 = nameFix2.replace("College", "")
			nameFix2 = nameFix2.replace("Elementary", "")
			nameFix2 = nameFix2.replace("High", "")
			nameFix2 = nameFix2.replace("Middle", "")

			print(nameFix2)

			schoolSearchString = 'http://nces.ed.gov/globallocator/index.asp?search=1&State=CA&city=' + cityfix + '&zipcode=&miles=&itemname=' + nameFix2 + '&sortby=name&School=1&PrivSchool=1'
			t = requests.request('Get', schoolSearchString)
			tempFile = open('testfile.txt', 'w')

			tempFileObject = t.text.encode('utf-8')


			
			tempFile.write(tempFileObject)
			tempFile.close()
			tempFile = open('testfile.txt', 'r')
			for line in tempFile:
				templine = line.strip('&')
				if searchterm in line:
					print ("can get gov info!")
					FoundSchool = True
					startPos = line.find("ID=")
					endPos = line.find("\');\">", startPos)
					schoolIdNumber = line[startPos+3:endPos]
					privateTest = 'Private'
					if privateTest in line:
						SchoolDataURL = "http://nces.ed.gov/surveys/pss/privateschoolsearch/school_detail.asp?Search=1" + '&SchoolID=' + schoolIdNumber +  "&ID=" + schoolIdNumber
						Private = "Yes"
					else:
						SchoolDataURL = "http://nces.ed.gov/ccd/schoolsearch/school_detail.asp?Search=1" + '&SchoolID=' + schoolIdNumber +  "&ID=" + schoolIdNumber
						Private = "No"

				
				


		tempFile.close()


		if FoundSchool:
			l = requests.request('Get', SchoolDataURL, headers = headers)
			g = open('tempFileForSchoolData.txt', 'w')
			g.write(l.text)
			g.close()
			g = open('tempFileForSchoolData.txt', 'r')
			print ("fetched")
			for line in g:
				if searchTerm_start_titleOne in line:
					startPos = line.find(searchTerm_start_titleOne)
					endPos = line.find(searchTerm_end_titleOne, startPos)
					titleOne = line[startPos + len(searchTerm_start_titleOne):endPos]
					print(titleOne)

				if searchTerm_start_titleOneProgram in line:
					startPos = line.find(searchTerm_start_titleOneProgram)
					endPos = line.find(searchTerm_end_titleOneProgram, startPos)
					titleOneProgram = line[startPos + len(searchTerm_start_titleOneProgram):endPos]
					print (titleOneProgram)

				if searchTerm_local_totalTeachers in line:
					for index in range(2):
						line2 = next(g)
					startPos = line2.find(searchTerm_start_totalTeachers)
					endPos = line2.find(searchTerm_end_totalTeachers, startPos)
					totalTeachers = line2[startPos + len(searchTerm_start_totalTeachers):endPos]
					print (totalTeachers)

				if searchTerm_local_totalStudents in line:
					for index in range(2):
						line2 = next(g)
					startPos = line2.find(searchTerm_start_totalStudents)
					endPos = line2.find(searchTerm_end_totalStudents, startPos)
					totalStudents = line2[startPos + len(searchTerm_start_totalStudents):endPos]
					print (totalStudents)

				if searchTerm_local_ratio in line:
					for index in range(2):
						line2 = next(g)
					startPos = line2.find(searchTerm_start_ratio)
					endPos = line2.find(searchTerm_end_ratio, startPos)
					ratio = line2[startPos + len(searchTerm_start_ratio):endPos]
					print (ratio)

				if searchTerm_start_freeLunch in line:
					startPos = line.find(searchTerm_start_freeLunch)
					endPos = line.find(searchTerm_end_freeLunch, startPos)
					freeLunch = line[startPos + len(searchTerm_start_freeLunch):endPos]
					print (freeLunch)

				if searchTerm_start_reducedLunch in line:
					startPos = line.find(searchTerm_start_reducedLunch)
					endPos = line.find(searchTerm_end_reducedLunch, startPos)
					reducedLunch = line[startPos + len(searchTerm_start_reducedLunch):endPos]
					print (reducedLunch)
			



			FoundSchool = False

		# a few fixes before the final write
		titleOneProgram = titleOneProgram.strip(';').strip('\n').strip('\r')
		titleOneProgram = titleOneProgram.replace(';', '')
		name = name.strip(';')
		titleOne = titleOne.strip(';')
		totalTeachers = totalTeachers.strip(';')
		totalStudents = totalStudents.strip(';')
		ratio = ratio.strip(';')
		freeLunch = freeLunch.strip(';')
		reducedLunch = reducedLunch.strip(';')



		CSVOutput = name + ";" + address + ";" + city + ";" + zipcode + ";" + dist + ';' + titleOne + ';' + titleOneProgram + ';' + totalTeachers + ';' + totalStudents + ';' + ratio + ';' + freeLunch + ';' + reducedLunch + ';' + Private
		CSVOutput = CSVOutput.strip('\n')
		CSVOutput = CSVOutput.encode('ascii', 'ignore').decode('ascii')
		CSVOutput = CSVOutput + '\n'
		writeFileCSV.write(CSVOutput)
		sleep(1)

main()
