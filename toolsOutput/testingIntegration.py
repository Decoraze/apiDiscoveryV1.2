import sys
from subprocess import run 
import subprocess
import os
from datetime import datetime
import PDFCSV.pdf as pdf

currentProcess = 0
def nuclei(textFile,link):
    #----------------------Nuclei---------------------#
    # Filtering#
    
    os.system("cp "+textFile + " toolsOutput/finalFindings/"+(str(link)+"/" ))                                             # copy output file over to finalfindings folder
                                                                            
    os.system("cat "+textFile+" | grep -v MSG > " + str(textFile)+"Filtered.txt")                                          # filter out any unneccessary message from ferox
    
    os.system(("nuclei -retries 3 -nc -l "+(str(textFile)+"Filtered.txt")+" >> "+(str(textFile) + "NucleiOutput.txt")))    # run nuclei command with max retries, silence, 
                                                                                                                           # and from a file given by feroxbuster and output the output to a text file

    os.system("cp "+(str(textFile) + "NucleiOutput.txt toolsOutput/finalFindings/"+(str(link)+"/" )))                      # copy the output from nuclei to finalfindings. 


    
def subfinder(sublink):

    #------------------SubDomain------------------#

    #command to run subdirectory finder to find all the subdirectories of the url that was given
    commandSubFinder = ["subfinder","-d",(str(sublink)),"-nW","-t","100","-o",("toolsOutput/outputFiles/"+str(sublink)+"Subfinder.txt")]
    
    #variable that stores the output of the subprocess and runs the command for subdirectory
    subfinder = subprocess.Popen(commandSubFinder, stdout=subprocess.PIPE ).communicate()[0]

    

def httpx(filePath,httpxLink):

    #---------------------HTTPX---------------------#
    #command to find the other rare ports that might be in use that is not the cmmon ports like 443, 8080 etc. 
    commandHttpx = ["httpx","-list",filePath, "-probe", "-sc", "-ip","-cl","-ct","-pa", "-nc","-o",("toolsOutput/outputFiles/"+str(httpxLink)+"Httpx.txt"),"-mc","200","-fc", "403,400,243,301"]#,"|","grep","200"]#add grepping for 200s and SUCCESS 
    #command to run the command given above by using subprocess library
    httpx = subprocess.Popen(commandHttpx, stdout=subprocess.PIPE).communicate()[0]

    try:
        commandStrip = ["cat", ("toolsOutput/outputFiles/"+str(httpxLink)+"Httpx.txt")]                                         # create command to cat the httpx output 
        strip = subprocess.Popen(commandStrip, stdout=subprocess.PIPE)                                                          # run the process
        commandGrep = ['grep','200']                                                                                            # grep only the those with 200 status codes
        output = subprocess.check_output((commandGrep), stdin=strip.stdout).decode("utf-8")
        #filtering even more by putting the output into a list and filtering from there using a nested loop
        outputlst = output.split("\n")                                                                                          # split the output into a list via \n
        links = []                                                                                                              # create a temporary variable for the lists to be returned later
        for requests in outputlst:                                                                                              # for loop to check which are the variables from the output that are actual links.
            link = (requests.split(' '))[0]

            if link not in links and link != '':                                                                                # appending links for returning to feroxbuster
                links.append(link)                                     # run the process and decode it into a vairbale output
    except:
        links = httpxLink
        
    
    return links                                                                                                            # return links for feroxbuster

def fileCheck(httpxlink):
    #check if the file is empty or the link provided has any subdomains.
    try:
        f = open((("toolsOutput/outputFiles/"+str(httpxlink))+"Subfinder.txt"),'r')                                         # opens file for subfinder to check if it is empty
        data = f.read()                                                                                                     # initialise  the file reading and get data from said file
                                                                                                          
        if data == '':                                                                                                      # if there is no file or if there is no data in the file, it will return True
            print("Link provided seems to not have any subdomains. Moving on to feroxbuster.")                              # Process message appears to tell that it is moving on to ferox instead of httpx
            return True
        else:
            print("Moving On to HTTPX")                                                                                     # if the file is populated, it moves onto httpx
            
            return False                                                                                                    # returning false in the process

    except FileNotFoundError:                                                                                               
        print("Internal Error!")
    except:
        print("Error!")
        
def command_group_run(url,recursions,list):
    now = datetime.now()
    time = now.strftime("%H%M%S")
    linkDir = (str(url)+str(time)+"/")
    os.system("mkdir toolsOutput/finalFindings/"+linkDir)
    #checks if the input has any values otherwise we set the default value. 
    if recursions != 0:
        try:
            numRecursions = int(recursions.strip(' '))
        except ValueError:
            numRecursions = 0
    elif recursions == 0:
        numRecursions = recursions
    if list != '':
        wordList = list.strip(' ')
    elif list == '':
        wordList = list
    try:
        subfinder(url)
        

        results = fileCheck(url)

        if results == False:
            os.system("cp toolsOutput/outputFiles/"+str(url)+"Subfinder.txt toolsOutput/finalFindings/"+linkDir)
            links = httpx(("toolsOutput/outputFiles/"+str(url)+"Subfinder.txt"),url)
            os.system("cp toolsOutput/outputFiles/"+str(url)+"Httpx.txt toolsOutput/finalFindings/"+linkDir)
            #---------------------FeroxBuster--------------------#
            if numRecursions == 0 or numRecursions == None:
                while True:
                    try:
                        numRecursions = int(input("Please input the number of times you want to do the recursion: "))
                        break
                    except ValueError:
                        print("Error! Wrong format! Please input numbers only!!")
            #checks if the file specififed by the user is available#
            fileFound = False
            while fileFound == False:
                if wordList == '' or wordList == None:
                    wordList = str(input("Please input the wordlist(include the path) you would want to use for the recursion: "))
                else:
                    print(wordList)
                try:
                    f = open(wordList)
                    fileFound = True
                            
                except FileNotFoundError:
                    print('Error! File is not found please try again!')
                    wordList = ''
            for urls in links:
                print(urls)
                commandFerox = ["feroxbuster","-u",urls,"-w",wordList,"-t","100","-f","-o","toolsOutput/outputFiles/"+(str(urls[8::])+"Feroxbuster.txt"),"--force-recursion","--time-limit","10m","--silent","-d",str(numRecursions),"-e"]
                feroxBuster = subprocess.Popen(commandFerox,stdout=subprocess.PIPE).communicate()[0]
                #call nuclei 
                nuclei("toolsOutput/outputFiles/"+(str(urls[8::])+"Feroxbuster.txt"),linkDir)

        elif results == True:
            #---------------------FeroxBuster--------------------#
            if numRecursions == 0:
                numRecursions = int(input("Please input the number of times you want to do the recursion: "))

            #checks if the file specififed by the user is available#
            fileFound = False
            while fileFound == False:
                if (wordList == '' or wordList == None) and numRecursions != 0:
                    wordList = str(input("Please input the wordlist(include the path) you would want to use for the recursion: "))
                    break
                else:
                    print(wordList)
                try:
                    f = open(wordList)
                    fileFound = True
                            
                except FileNotFoundError:
                    print(wordList)
                    print('Error! File is not found please try again!')
                    wordList = ''
            
            print(url)
            commandFerox = ["feroxbuster","-u",url,"-w",wordList,"-t","100","-f","-o","toolsOutput/outputFiles/"+(str(url)+"Feroxbuster.txt"),"--force-recursion","--time-limit","10m","--silent","-d",str(numRecursions),"-e"]
            feroxBuster = subprocess.Popen(commandFerox,stdout=subprocess.PIPE).communicate()[0]
            #call nuclei 
            nuclei("toolsOutput/outputFiles/"+(str(url)+"Feroxbuster.txt"),linkDir)
        commandCleanUp = ["rm","-r","toolsOutput/outputFiles/"]
        cleanUp = subprocess.Popen(commandCleanUp,stdout=subprocess.PIPE).communicate()[0]
    except KeyboardInterrupt:
        #cleanup
        commandCleanUp = ["rm","-r","toolsOutput/outputFiles/"]
        cleanUp = subprocess.Popen(commandCleanUp,stdout=subprocess.PIPE).communicate()[0]
        returnVariables = [url]
        
        if numRecursions != 0:
            returnVariables.append(numRecursions)
        else:
            returnVariables.append(None)
        if wordList != '':
            returnVariables.append(wordList)
        else:
            returnVariables.append(None)

        return returnVariables

    os.system("clear")
    pdf.main(linkDir,url)
    os.system("echo 'Finished Scanning'")

def main(link,numRec,wordl):
    print("Now Running Subfinder --> HTTPX --> FeroxBuster --> Nuclei!!")
    try:
        flag = False

        while flag == False:
            x = input("Continue?(Yes [y] or No [n]) : ")

            if x.lower() == "y" or x.lower() == "yes" :
                #link = input("Please input the url you want to use. E.g. twiiter.com/facebook.com/thedogapi.com: ")
                run = command_group_run(link,numRec,wordl)
                flag = True
            elif x.lower() == "n" or x.lower() == "no":
                print("Exiting Program.")
                return False
                flag = True
            else:
                print("Error has occured. Please Enter your choice again!")
                
    except ValueError:
        print("An Error Has Occured.")
    
    return run