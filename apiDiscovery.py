#import files and libraries
import os
import sys
import toolsOutput.testingIntegration as toolsIntegration
import subprocess
from subprocess import run
import argparse
import PDFCSV.pdf as pdf


def main():
    #check for dependancies installed on the system.
    os.system("chmod 777 dependancyChecker.sh")
    os.system("./dependancyChecker.sh")
    ###
    

    flag = False

    while flag != True:
        try:

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
                            if line != "":
                                data = line[1:-2]
                                data = data.split(',')
                                numRec = data[1]
                                wordl = data[2]
                                url = data[0]
                                passCheck = True
                                print("Warning! Deleting Saved Inputs from your previous session!")
                                file.close()
                                savedInputDelete = ["rm",str(url)+defaultFileName]
                                savedInputCleanUp = subprocess.Popen(savedInputDelete,stdout=subprocess.PIPE).communicate()[0]
                            else:
                                print("Data from your previous session was not saved properly!")
                        elif userInput.lower() == 'no':
                            file.close()
                            print("Warning! Deleting Saved Inputs from your previous session!")
                            savedInputDelete = ["rm",str(url)+defaultFileName]
                            savedInputCleanUp = subprocess.Popen(savedInputDelete,stdout=subprocess.PIPE).communicate()[0]
                            passCheck = True

            except FileNotFoundError:
                None

            #CSV/PDF
            if usrInput == "w":
                print("You chose to output a pdf and or csv file!")
                pdf.main(url)

            elif usrInput == "t":
                print("You chose to use the tools!")
                try:
                    commandRun = toolsIntegration.main(url,numRec,wordl)
                    
                    if type(commandRun) == list:
                        
                        
                        os.system("echo "+str(commandRun)+" > "+ str(url)+ defaultFileName)
                    flag = True
                    
                except KeyboardInterrupt:
                    print("\nThe program has stopped unexpectedly! Please check your inputs and ensure that your inputs are valid(unless you ctrl c then thats fine).")
                    flag = True
                    #clean up on event of crashing
                    try:
                        f = os.listdir("toolsOutput/outputFiles/")
                        commandCleanUp = ["rm","-r","toolsOutput/outputFiles/"]
                        cleanUp = subprocess.Popen(commandCleanUp,stdout=subprocess.PIPE).communicate()[0]
                    except FileNotFoundError:
                        print("")
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

