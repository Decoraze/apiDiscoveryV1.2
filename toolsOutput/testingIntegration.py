
from subprocess import run 
import subprocess
import os

currentProcess = 0
def nuclei(textFile):
    #----------------------Nuclei---------------------#
    # Filtering#
            
    #nucleiTemplates = str(input("Please input the template you want to use for the testing.E.g. /nuclei-templates/...: " ))
    #command = ("cat "+textFile+" | grep -v MSG > " + str(textFile)+"Filtered.txt")
    
    os.system("cat "+textFile+" | grep -v MSG > " + str(textFile)+"Filtered.txt")
    commandNuclei = ["nuclei","-l",(str(textFile)+"Filtered.txt")]
    runNuclei = subprocess.Popen(commandNuclei, stdout=subprocess.PIPE ).communicate()[0]

    
def subfinder(sublink):

    #------------------SubDomain------------------#

    #command to run subdirectory finder to find all the subdirectories of the url that was given
    commandSubFinder = ["subfinder","-d",(str(sublink)),"-nW","-t","100","-o",("toolsOutput/outputFiles/"+str(sublink)+"Subfinder.txt")]
    #output = run(command, capture_output=True).stdout
    #variable that stores the output of the subprocess and runs the command for subdirectory
    subfinder = subprocess.Popen(commandSubFinder, stdout=subprocess.PIPE ).communicate()[0]

def httpx(filePath,httpxLink):

    #---------------------HTTPX---------------------#
    #command to find the other rare ports that might be in use that is not the cmmon ports like 443, 8080 etc. 
    commandHttpx = ["httpx","-list",filePath, "-probe", "-sc", "-ip","-cl","-ct","-pa", "-nc","-o",("toolsOutput/outputFiles/"+str(httpxLink)+"Httpx.txt"),"-mc","200","-fc", "403,400,243,301"]#,"|","grep","200"]#add grepping for 200s and SUCCESS 
    #command to run the command given above by using subprocess library
    httpx = subprocess.Popen(commandHttpx, stdout=subprocess.PIPE).communicate()[0]

    #command to filter the output: cat *url*Httpx.txt | grep 200
    commandStrip = ["cat", ("toolsOutput/outputFiles/"+str(httpxLink)+"Httpx.txt")]
    strip = subprocess.Popen(commandStrip, stdout=subprocess.PIPE)
    commandGrep = ['grep','200']
    output = subprocess.check_output((commandGrep), stdin=strip.stdout).decode("utf-8")
    
    
        #print(type(output))testing
        
    #filtering even more by putting the output into a list and filtering from there using a nested loop
    outputlst = output.split("\n")
    links = []
    for requests in outputlst:
        link = (requests.split(' '))[0]

        if link not in links and link != '':
            links.append(link)
    return links

def fileCheck(httpxlink):
    #check if the file is empty or the link provided has any subdomains.
    try:
        f = open((("toolsOutput/outputFiles/"+str(httpxlink))+"Subfinder.txt"),'r')
        data = f.read()
        print(data == '')
        if data == '':
            print("Link provided seems to not have any subdomains. Moving on to feroxbuster.")
            return True
        else:
            print("Moving On to HTTPX")
            
            return False

    except FileNotFoundError:
        print("Internal Error!")

def command_group_run(url,recursions,list):
    if recursions != 0:
        numRecursions = int(recursions.strip(' '))
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
            links = httpx(("toolsOutput/outputFiles/"+str(url)+"Subfinder.txt"),url)
            
            #---------------------FeroxBuster--------------------#
            if numRecursions == 0 or numRecursions == None:
                numRecursions = int(input("Please input the number of times you want to do the recursion: "))
            
            #wordList = str(input("Please input the wordlist(include the path) you would want to use for the recursion: "))

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
                commandFerox = ["feroxbuster","-u",urls,"-w",wordList,"-t","100","-f","-o","toolsOutput/outputFiles/"+(str(urls[8::])+"Feroxbuster.txt"),"--force-recursion","--time-limit","20m","--silent","-d",str(numRecursions),"-e"]
                feroxBuster = subprocess.Popen(commandFerox,stdout=subprocess.PIPE).communicate()[0]
                #call nuclei 
                nuclei("toolsOutput/outputFiles/"+(str(urls[8::])+"Feroxbuster.txt"))

        elif results == True:
            #---------------------FeroxBuster--------------------#
            if numRecursions == 0:
                numRecursions = int(input("Please input the number of times you want to do the recursion: "))
            
            #wordList = str(input("Please input the wordlist(include the path) you would want to use for the recursion: "))

            #checks if the file specififed by the user is available#
            fileFound = False
            while fileFound == False:
                if numRecursions == '':
                    wordList = str(input("Please input the wordlist(include the path) you would want to use for the recursion: "))
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
            commandFerox = ["feroxbuster","-u",url,"-w",wordList,"-t","100","-f","-o","toolsOutput/outputFiles/"+(str(url)+"Feroxbuster.txt"),"--force-recursion","--time-limit","20m","--silent","-d",str(numRecursions),"-e"]
            feroxBuster = subprocess.Popen(commandFerox,stdout=subprocess.PIPE).communicate()[0]
            #call nuclei 
            nuclei("toolsOutput/outputFiles/"+(str(url)+"Feroxbuster.txt"))
        
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
        #print(returnVariables)
        return returnVariables
        
        
        #print(links) #use this for testing 

    

def main(link,numRec,wordl):
    #link = input("Please input the url you want to use. E.g. twiiter.com/facebook.com/thedogapi.com: ")
    run = command_group_run(link,numRec,wordl)
    return run

#if __name__ == "__main__":
#    main()