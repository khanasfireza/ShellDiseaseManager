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
        "4 to for Setting and Changing Patient Statusn\n5 - Search for patient\nType 6 to quit")
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
        while True:
            print("A - East\nB - West\nC - North\nD - South")
            zone = input("Zone: ")
            if zone == 'A' or zone == 'B' or zone == 'C' or zone == 'D':
                break
            else:
                continue

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

        print("Optional Info[Not Required]\nWrite symptoms separated by comma E.G: Cough,Fever,Pain")
        inp = input("Current Symptoms: ")
        currentSymptoms = [each for each in inp.split(',')]
        medicalHistory = input("Medical History: ")
        DateOfBirth = input("Date of birth: ")

        # Register the user in the text file
        read_write_file('PatientInfo.txt',
                        f"name:{name},age:{age},registration_time:{datetime.now().strftime('%d/%m/%Y %H:%M:%S')},email:{email},mobile_number:{mobile_number},zone:{zone},address:{address},group:{group}")

        read_write_file("PatientCase.txt", f"name:{name},status:active,zone:{zone}")

        read_write_file("OptionalPatientInfo.txt",
                        f"name:{name},registration_time:{datetime.now().strftime('%d/%m/%Y %H:%M:%S')},current_symptoms:{currentSymptoms},medical_history:{medicalHistory},date_of_birth:{DateOfBirth}")

        print(f"{'-' * 25}")


    # Provides test information and saves test information in test file
    elif option == "2":
        print(f"{'-' * 25}")
        patient_name = input("Patient Name: ").lower()
        patient_id = input("Patient Id: ").lower()
        while True:
            test_number = input("Test Number: ").lower()
            if test_number == '1' or test_number == '2' or test_number == '3':
                break
            else:
                continue
        print("Write \"positive\" or \"negative\"")
        test_result = input("Test Result: ").lower()
        patientFileData = readFileData('PatientInfo.txt')
        reducedData = [i for i in patientFileData if patient_name in i and patient_id in i]
        action = ""
        group = ""
        if len(reducedData) == 0:
            print('No paitent found')
        else:

            group = reducedData[0].split('group:')[1]
            if "ATO" in group or "ACC" in group or "AEO" in group:
                if test_result == 'positive':
                    action = 'QHNF'
                elif test_result == 'negative' and (test_number == '1' or test_number == '2'):
                    action = 'QDFR'
                elif test_result == 'negative' and test_number == '3':
                    action = 'RU'
            elif "SID" in group:
                if test_result == 'positive':
                    action = 'QHNF'
                elif test_result == 'negative' and (test_number == '1' or test_number == '2'):
                    action = 'HQFR'
                elif test_result == 'negative' and test_number == '3':
                    action = 'RU'
            elif "AHS" in group:
                if test_result == 'positive':
                    action = 'HQNF'
                elif test_result == 'negative' and (test_number == '1' or test_number == '2'):
                    action = 'CWFR'
                elif test_result == 'negative' and test_number == '3':
                    action = 'CW'

        read_write_file(f'Test{test_number}.txt',
                        f"name:{patient_name},id:{patient_id},action:{action},result:{test_result},group:{group}",
                        id=False)

    # Prints Statistics
    elif option == '3':

        # Read Files and saves in var
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
            f"Total Recovered Cases: {recoveredCases}\n")
        print(f"{'-' * 25}")

    # Changing status of patient
    elif option == '4':
        patient_name = input("Patient Name: ").lower()
        patient_id = input("Patient Id: ").lower()
        print("Write 1.\"active\" if the case is active or 2.\"recovered\" if the patient is recovered "
              "3.\"deceased\" if the case is recovered ")
        while True:
            patient_status = input("Patient Status: ").lower()
            if patient_status == 'active' or patient_status == 'recovered' or patient_status == 'deceased':
                break
            else:
                print("Please write between those 3 options")
                continue
        patientCaseFile = readFileData('PatientCase.txt')
        reducedData = [i for i in patientCaseFile if
                       patient_name == re.search("name:(.+?),", i).group(1) and patient_id == re.search("id:(.+?),",
                                                                                                        i).group(1)]
        zone = ''
        print(reducedData)
        if len(reducedData) == 0:
            print("Patient Not Found")
        else:
            for each in reducedData:
                zone = re.search("zone:(.+?)", each).group(1)
                patientCaseFile.remove(each)
            print(patientCaseFile)
            read_write_file('PatientCase.txt',
                            f"id:{patient_id},name:{patient_name},status:{patient_status},zone:{zone}",
                            listedData=patientCaseFile, id=False)


    elif option == '5':
        patient_name = input("Patient Name: ").lower()
        patient_id = input("Patient Id: ").lower()
        patientCaseFile = readFileData('PatientCase.txt')
        patientInfoFile = readFileData('PatientInfo.txt')
        reducedCaseData = [i for i in patientCaseFile if
                           patient_name == re.search("name:(.+?),", i).group(1) and patient_id == re.search("id:(.+?),",
                                                                                                            i).group(1)]
        reducedInfoData = [i for i in patientInfoFile if
                           patient_name == re.search("name:(.+?),", i).group(1) and patient_id == re.search("id:(.+?),",
                                                                                                            i).group(1)]
        if len(reducedCaseData) == 0 and len(reducedInfoData) == 0:
            print("No Patient Found")
        else:
            print(
                f"Patient Name: {patient_name}\nPatient id: {patient_id}\nCase id: {patient_id}\nPatient Status: {re.search('status:(.+?);', reducedCaseData[0])}")
    elif option == '6':
        break


