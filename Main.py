"""
To run use Python3.7+
Do not tamper the text file,
Text file is used as database,
Patient Case - saves case of patient and shows if the case is active or not
Patient Info - saves all patient info after registration
Optional Patient info - saves all patient optional information
Test 1 - saves test-1 results
Test 2 - saves test-2 results
Test 3 - saves test-3 results

"""


import re
from datetime import datetime
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


# Please run this code using cmd or powershell or terminal
# This function reads text file and writes to them
def read_write_file(filename, data, id=True, listedData=None):
    # filename is the name of the text file, data is the value that needs to be written in the file,
    # listedData is the provided array, id signifies if the function provide a unique id

    # Opening the file and reading the file
    with open(filename, 'r') as patientFile:
        if listedData is None:
            # Data of all patient is saved in patient and listed data contains all the patient info as list element
            patient = patientFile.read()
            listedData = patient.split(';\n')

        # Removes all the empty element from the array
        while "" in listedData:
            listedData.remove("")
        # Removes all the empty line-escape element from the array
        while "\n" in listedData:
            listedData.remove("\n")
        # If id is true then it will provide a unique id, if false then not
        if id:
            # appending the given data in the array
            listedData.append(f"id:{len(listedData) + 1},{data}")
            listedData.sort()
        else:
            listedData.append(f"{data}")
        with open(filename, 'w') as writeToFile:
            # looping through all the data in the array and writing it in the text file
            for eachItem in listedData:
                writeToFile.write(f"{eachItem};\n")
            writeToFile.close()
        patientFile.close()
    return len(listedData) + 1


# This functions read a text file and returns a list of elements
def readFileData(filename):
    with open(filename, 'r') as patientFile:
        patientData = patientFile.read()
        listedData = patientData.split(';\n')
        while "" in listedData:
            listedData.remove("")
        while "\n" in listedData:
            listedData.remove("\n")
        patientFile.close()
        return listedData


"""
1 - Patient Registration
2 - Test Action
3 - Statistics
4 - Changing patient status
5 - Patient Status
"""

while True:
    # User provided input for the option
    print(f"{'-' * 25}")
    print(
        "Type 1 for patient Registration\nType 2 for Inputting Test Results and Action\nType 3 to Get Statistics\nType "
        "4 to for Setting and Changing Patient Statusn\nType 5 Search for patient\nType 6 to quit")
    print(f"{'-' * 25}")
    option = input(">")
    if option == "1":
        while True:
            print(f"Required Information. Please fill up the following inputs")

            name = input("Name:").lower()

            # If age is not a number it will show that msg and ask for age again
            while True:
                age = input("Age:").lower()
                if age.isnumeric():
                    break
                else:
                    print('Please enter a valid age')
                    continue
            # If mobile number doesnt contain any number and less than 9 it will ask for it again
            while True:
                mobile_number = input("Mobile Number:").lower()
                if mobile_number.isnumeric() and len(mobile_number) < 14:
                    break
                else:
                    print('Please provide a valid mobile number')
            # Email validation
            while True:
                email = input("Email:").lower()
                if '@' in email and '.com' in email:
                    break
                else:
                    print('Please enter a valid email')
                    continue
            address = input("Address:").lower()
            # All these fields are required if not filled it will ask again
            if name == '' and age == '' and email == '' and mobile_number == '':
                print("Please fill up all the form to proceed")
                continue
            break
        # zone
        while True:
            print("A - East\nB - West\nC - North\nD - South")
            zone = input("Zone: ")
            if zone == 'A' or zone == 'B' or zone == 'C' or zone == 'D':
                break
            else:
                continue
        # group
        while True:
            print("Write =>\nATO = Asymptomatic individuals with history of travelling overseas \nACC = Asymptomatic "
                  "individuals with history of contact with known case of COVID-19\nAEO = Asymptomatic individuals "
                  "who had attended event associated with known COVID-19 outbreak\nSID = Symptomatic individuals\nAHS "
                  "= Asymptomatic hospital staff")
            group = input("Group: ")
            if group == 'ATO' or group == 'ACC' or group == 'AEO' or group == 'SID' or group == 'AHS':
                break
            else:
                continue
        # Optional data
        print("Optional Info[Not Required]\nWrite symptoms separated by comma E.G: Cough,Fever,Pain")
        inp = input("Current Symptoms: ")
        currentSymptoms = [each for each in inp.split(',')]
        medicalHistory = input("Medical History: ")
        DateOfBirth = input("Date of birth: ")

        # Register the user in the text file patient data saved into "PatientInfo.txt" data-format: id:[
        # auto-generated],name:[patient_name],reg_time:[current-date-time],email:[current_email],mob_num:[mob_num],
        # zone:[zone], address:[address], group:[group] and every patient data is separated with comma and space
        current_date_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        p_id = read_write_file('PatientInfo.txt',
                               f"name:{name},age:{age},registration_time:{current_date_time},email:{email},mobile_number:{mobile_number},zone:{zone},address:{address},group:{group}")
        # patient case saved into "PatientCase.txt"
        read_write_file("PatientCase.txt", f"pid:{p_id},name:{name},status:active,zone:{zone}")
        # patient optional data saved into "PatientOptionalInfo.txt"
        read_write_file("OptionalPatientInfo.txt",
                        f"name:{name},registration_time:{datetime.now().strftime('%d/%m/%Y %H:%M:%S')},current_symptoms:{currentSymptoms},medical_history:{medicalHistory},date_of_birth:{DateOfBirth}")
        print(f"New patient created: \nPatient name: {name}\nPatient id:{p_id}\nRegistration Time:{current_date_time}")

        print(f"{'-' * 25}")


    # Provides test information and saves test information in test file
    elif option == "2":
        print(f"{'-' * 25}")
        # asks for user input
        patient_name = input("Patient Name: ").lower()
        patient_id = input("Patient Id: ").lower()
        # validation for test number only work if input is 1,2 or 3
        while True:
            test_number = input("Test Number: ").lower()
            if test_number == '1' or test_number == '2' or test_number == '3':
                break
            else:
                continue
        # validation for test result, only work if positive or negative
        print("Write \"positive\" or \"negative\"")
        while True:
            test_result = input("Test Result: ").lower()
            if test_result == 'positive' or test_result == 'negative':
                break
            else:
                continue
        # Read file data and return an array
        patientFileData = readFileData('PatientInfo.txt')

        # reduced data where only the patient with valid name and id is available
        reducedData = [i for i in patientFileData if
                       patient_name == re.search("name:(.+?),", i).group(1) and patient_id == re.search("id:(.+?),",
                                                                                                        i).group(1)]
        # declaring action and group var
        action = ""
        group = ""
        # if no such patient and patient id is available it will show no patient found
        if len(reducedData) == 0:
            print('No paitent found')
        else:
            # if it finds the patient then set the group-var as per the patient group
            group = reducedData[0].split('group:')[1]
            # logic as per table-2

            # logic for group acc,ato and aeo
            if "ATO" in group or "ACC" in group or "AEO" in group:
                # if test-result is positive
                if test_result == 'positive':
                    action = 'QHNF'
                # if test-result is negative and test number is either 1 or 2
                elif test_result == 'negative' and (test_number == '1' or test_number == '2'):
                    action = 'QDFR'
                # if test-result is negative and test number is 3
                elif test_result == 'negative' and test_number == '3':
                    action = 'RU'
            # logic for the group sid
            elif "SID" in group:
                if test_result == 'positive':
                    action = 'QHNF'
                elif test_result == 'negative' and (test_number == '1' or test_number == '2'):
                    action = 'HQFR'
                elif test_result == 'negative' and test_number == '3':
                    action = 'RU'
            # logic for the group ahs
            elif "AHS" in group:
                if test_result == 'positive':
                    action = 'HQNF'
                elif test_result == 'negative' and (test_number == '1' or test_number == '2'):
                    action = 'CWFR'
                elif test_result == 'negative' and test_number == '3':
                    action = 'CW'
        # read the file and write the test to it
        read_write_file(f'Test{test_number}.txt',
                        f"name:{patient_name},id:{patient_id},action:{action},result:{test_result},group:{group}",
                        id=False)
        print(f"{'-' * 25}")
    # Prints Statistics
    elif option == '3':
        print(f"{'-' * 25}")
        # Read Files and saves in variables
        testFile1 = readFileData('Test1.txt')
        testFile2 = readFileData('Test2.txt')
        testFile3 = readFileData('Test3.txt')
        patientCases = readFileData('PatientCase.txt')

        # calculates all cases
        activeCases = len([ac for ac in patientCases if 'active' in ac])
        recoveredCases = len([rc for rc in patientCases if 'recovered' in rc])
        deceasedCases = len([dc for dc in patientCases if 'deceased' in dc])

        # calculates patient cases and info
        total_test_done = len(testFile1) + len(testFile2) + len(testFile3)
        total_patient = len(readFileData('PatientInfo.txt'))
        total_positive_cases = len([i for i in testFile1 if 'positive' in i]) + len(
            [i for i in testFile2 if 'positive' in i]) + len([i for i in testFile3 if 'positive' in i])

        # calculates zonal info
        aZoneCases = len([ac for ac in patientCases if 'active' in ac and 'a' == re.search("zone:(.+?);", ac)])
        bZoneCases = len([ac for ac in patientCases if 'active' in ac and 'b' == re.search("zone:(.+?);", ac)])
        cZoneCases = len([ac for ac in patientCases if 'active' in ac and 'c' == re.search("zone:(.+?);", ac)])
        dZoneCases = len([ac for ac in patientCases if 'active' in ac and 'd' == re.search("zone:(.+?);", ac)])


        # function to calculate number according to group
        def getNumber(group):
            return len([i for i in testFile1 if 'positive' in i and f'{group}' in i]) + len(
                [i for i in testFile2 if 'positive' in i and f'{group}' in i]) + len(
                [i for i in testFile3 if 'positive' in i and f'{group}' in i])


        # calculates group info
        atoGrpCase = getNumber('ATO')
        accGrpCase = getNumber('ACC')
        aeoGrpCase = getNumber('AEO')
        sidGrpCase = getNumber('SID')
        ahsGrpCase = getNumber('AHS')
        print(f"{'-' * 25}\n")
        print(
            f"Total Patient: {total_patient}\nTotal Test Done: {total_test_done}\nTotal Positive Cases: {total_positive_cases}\n"
            f"East zone active cases: {aZoneCases} "f"\nWest zone active cases: {bZoneCases}\nNorth zone active cases: {cZoneCases}\nSouth zone active cases: {dZoneCases}\n"
            f"ATO Group Positive Cases: {atoGrpCase}\n"
            f"ACC Group Positive Cases: {accGrpCase}\n"
            f"AEO Group Positive Cases: {aeoGrpCase}\n"
            f"SID Group Positive Cases: {sidGrpCase}\n"
            f"AHS Group Positive Cases: {ahsGrpCase}\n"
            f"Total Recovered Cases: {recoveredCases}\n"
            f"Total Active Cases: {activeCases}\n"
            f"Total deceased Cases: {deceasedCases}\n")
        print(f"{'-' * 25}")
        # output format =>
        """-------------------------
        Total Patient: 45
        Total Test Done: 24
        Total Positive Cases: 12
        East zone active cases: 5 
        West zone active cases: 3
        North zone active cases: 5
        South zone active cases: 5
        ATO Group Positive Cases: 3
        ACC Group Positive Cases: 4
        AEO Group Positive Cases: 1
        SID Group Positive Cases: 2
        AHS Group Positive Cases: 2
        Total Recovered Cases: 5
        Total Active Cases: 6
        Total deceased Cases: 7
        -------------------------
        """
    # Changing status of patient
    elif option == '4':
        # getting input of the patient and his id
        print(f"{'-' * 25}")
        patient_name = input("Patient Name: ").lower()
        patient_id = input("Patient Id: ").lower()
        print("Write 1.\"active\" if the case is active or 2.\"recovered\" if the patient is recovered "
              "3.\"deceased\" if the case is recovered ")
        # asks for status and a validation checks if the input is correct
        while True:
            patient_status = input("Patient Status: ").lower()
            if patient_status == 'active' or patient_status == 'recovered' or patient_status == 'deceased':
                break
            else:
                print("Please write between those 3 options")
                continue
        # read file
        patientCaseFile = readFileData('PatientCase.txt')
        # searches the file and checks for the searched user
        reducedData = [i for i in patientCaseFile if
                       patient_name == re.search("name:(.+?),", i).group(1) and patient_id == re.search("pid:(.+?),",
                                                                                                        i).group(1)]
        zone = ''
        print(reducedData)
        if len(reducedData) == 0:
            print("Patient Not Found")
        else:
            # set the zone
            for each in reducedData:
                zone = re.search("zone:(.+?)", each).group(1)
                patientCaseFile.remove(each)
            # read and writes to file
            read_write_file('PatientCase.txt',
                            f"id:{patient_id},name:{patient_name},status:{patient_status},zone:{zone}",
                            listedData=patientCaseFile, id=False)
        print(f"{'-' * 25}")
    # searches for patient
    elif option == '5':
        # takes patient name and id
        print(f"{'-' * 25}")
        patient_name = input("Patient Name: ").lower()
        patient_id = input("Patient Id: ").lower()
        # reads the file
        patientCaseFile = readFileData('PatientCase.txt')
        patientInfoFile = readFileData('PatientInfo.txt')
        # searches for patient
        reducedCaseData = [i for i in patientCaseFile if
                           patient_name == re.search("name:(.+?),", i).group(1) and patient_id == re.search(
                               "pid:(.+?),",
                               i).group(1)]
        reducedInfoData = [i for i in patientInfoFile if
                           patient_name == re.search("name:(.+?),", i).group(1) and patient_id == re.search("id:(.+?),",
                                                                                                            i).group(1)]
        # if patient is not valid or found
        if len(reducedCaseData) == 0 and len(reducedInfoData) == 0:
            print("No Patient Found")
        else:

            print(
                f"Patient Name: {patient_name}\nPatient id: {patient_id}\nCase id: {patient_id}\nPatient Status: {re.search('status:(.+?),', reducedCaseData[0]).group(1)}")
        print(f"{'-' * 25}")
    # quit code exits the script

    elif option == '6':
        print(f"{'-' * 25}")
        i = input("Press enter to exit if you dont want to quit press 1")
        if i == '1':
            print(f"{'-' * 25}")
            continue
        else:
            print("Quitting the program")
            print(f"{'-' * 25}")
            break

