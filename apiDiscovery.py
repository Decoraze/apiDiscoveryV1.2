#import files and libraries
import os
import sys
import toolsOutput.testingIntegration as toolsIntegration
import subprocess
from subprocess import run
import argparse



def main():
    #check for dependancies installed on the system.
    os.system("chmod 777 dependancyChecker.sh")
    os.system("./dependancyChecker.sh")
    ###
    

    flag = False

    while flag != True:
        try:

            #usrInput = input("Please enter your command here(type -h for the list of commands):  ").lower() #user input
            parser = argparse.ArgumentParser(description="takes in user's url input")
            parser.add_argument('url', metavar='url',type=str, help='enter your url')
            parser.add_argument('choice',metavar='choice',type=str,help='Enter your Choices. \n'
            't: To use tools for Discovery,\n'
            'w: To write to PDF/CSV,\n'
            'q: To Quit')
            args = parser.parse_args()

            url = args.url
            usrInput = args.choice
            
            numRec = 0
            wordl = ''

            defaultFileName = 'savedInput.txt'

            #check for savedInput file
            try:
                with open(str(url)+defaultFileName,'r') as file:
                    passCheck = False
                    while passCheck == False:
                        userInput = input('Do you want to continue with the previously saved information?(Yes or No)') #add error handling here later

                        if userInput.lower() == 'yes':
                            line = file.readline()
                            data = line[1:-2]
                            data = data.split(',')
                            numRec = data[1]
                            wordl = data[2]
                            url = data[0]
                            passCheck = True
                            print("Warning! Deleting Saved Inputs from your previous session!")
                            savedInputDelete = ["rm",str(url)+defaultFileName]
                            savedInputCleanUp = subprocess.Popen(savedInputDelete,stdout=subprocess.PIPE).communicate()[0]
                        elif userInput.lower() == 'no':
                            file.close()
                            print("Warning! Deleting Saved Inputs from your previous session!")
                            savedInputDelete = ["rm",str(url)+defaultFileName]
                            savedInputCleanUp = subprocess.Popen(savedInputDelete,stdout=subprocess.PIPE).communicate()[0]
                            passCheck = True

            except FileNotFoundError:
                None
            print("")
            #help page
            if usrInput == "h":
                print("----------------------------------------------------------------------------------------------------------------------\n"
                "Welcome to the API Discovery Help Page! Here are the list of commands:\n"
                "b         Brute Force Method using a specified wordlist and url\n"
                "o         Output to a readable csv/excel/pdf file. (Can only be done after using the other methods of enumeration\n"
                "t         Using tools (Subfinder,Nuclei etc) to recursively find and test the web links/api links found (if any)\n"
                "q         To quit the program\n"
                "----------------------------------------------------------------------------------------------------------------------\n")
                
            #function 1: brute force
            #elif usrInput == "b":
            #    print("you chose the brute force method!")
            #    apiTest.apiTest()
            #function 2: output to csv & pdf file  
            #elif usrInput == "-o":
            #    print("Outputted to CSV & PDF File. This file can be found under the export files file as output.csv and output.pdf")
            #    eF.main()
            #function 4: 

            #function (x): quit 

            #CSV/PDF
            elif usrInput == "w":
                print("You chose to output a pdf and or csv file!")


            elif usrInput == "t":
                print("You chose to use the tools!")
                try:
                    commandRun = toolsIntegration.main(url,numRec,wordl)
                    
                    if type(commandRun) == list:
                        
                        #print("echo '["+str(commandRun)+"]' > testfile.txt")
                        os.system("echo "+str(commandRun)+" > "+ str(url)+ defaultFileName)
                    flag = True
                except KeyboardInterrupt:
                    print("\nThe program has stopped unexpectedly! Please check your inputs and ensure that your inputs are valid(unless you ctrl c then thats fine).")
                    flag = True
                    #clean up on event of crashing
                    commandCleanUp = ["rm","-r","toolsOutput/outputFiles/"]
                    cleanUp = subprocess.Popen(commandCleanUp,stdout=subprocess.PIPE).communicate()[0]
                
            elif usrInput == "q":
                print("Ending Program!")
                sys.exit()
            else:
                print("Please use the specified options! Thanks")
        #error handling
        except KeyboardInterrupt:
            print("\nThe program has stopped unexpectedly! Please check your inputs and ensure that your inputs are valid(unless you ctrl c then thats fine).")
            flag = True
            #clean up on event of crashing
            commandCleanUp = ["rm","-r","toolsOutput/outputFiles/"]
            cleanUp = subprocess.Popen(commandCleanUp,stdout=subprocess.PIPE).communicate()[0]
    return None

#run main function if main function is found 
if __name__ == "__main__":
    main()

