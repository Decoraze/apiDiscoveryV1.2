#imports
import requests as req
import sys
import os
from stopit import threading_timeoutable as timeoutable

#get a wordlist from a specified path
def getWordlist(path):
    try:
        #open file path, read the file contents and split it between
        #to put the items into a list
        with open(path,"r") as f:
            wordlist = (f.read()).split("\n")
            return wordlist
        
    except FileNotFoundError:
        print("FileNotFound! Please check your file name!")
        sys.exit()
        
#clear output text files
def clearLogs():
    try:
        with open("acceptedLinks.txt","r") as f:
            data = f.readlines()

        with open("acceptedLinks.txt","w") as f:
            for line in data:
                f.write('')

    except ValueError:
        print("FileNotFound! Please check that you have the file: accecptedLinks and acceptedLinksOutput!")
        sys.exit()

def apiDetailsFromAcceptedLinks(lst):
    try:
        fileSize = os.stat("acceptedLinks.txt").st_size
    except FileNotFoundError:
        print("FileNotFound! Please check that you have the file: accecptedLinks and acceptedLinksOutput!")
        sys.exit()

    #check to see whether the file is empty of not. 
    while fileSize != 0:
        links = getWordlist("acceptedLinks.txt")

        #concat links and endpoints to get new urls
        for x in range (len(links)):
            l = links[x]
            if l != '' and ((l[::-11]) != "favicon.ico"):
                for ep in lst:
                    url = str(l)+"/"+str(ep)
                    print(url)

                    output = apiDetails(url)
                    if output != None: 
                        with open("output.txt","a") as f:
                            #print(tempLink) #uncomment this when you want to test the links and whether it is iterating the list 
                            f.write(output)
                            
        clearLogs()
        wl = getWordlist("acceptedLinksOutput.txt")
        with open("acceptedLinks.txt","w") as f:
            for i in wl:
                if i not in links:
                    f.write(i+"\n")
        #break #add this for testing purposes 
                                    
#get details and response of the requested link
def apiDetails(link):
    try:
        response = req.get(link)
        
        message = ""
        
        if response.reason == "OK":
            #general try function for everything else other than an image
            try:
                json = response.json()
                if json == {} or json == [] or json == ():
                    print("Empty Link: ",link)
                else:
                    responseReq = response.request
                    #Normal Response e.g. 200, 300, 400
                    message += "\nResponse: "+ str(response)+"\n"
                    #API Response URL
                    message += "Response Path: "+ str(response.url)+"\n"
                    print("URL Accepted: ",response.url,"\n\n")
                    with open("acceptedLinks.txt","a") as f:
                        f.write(str(response.url)+"\n")
                    aLO = getWordlist("acceptedLinksOutput.txt")
                    
                    if (str(response.url)) not in aLO:
                        with open("acceptedLinksOutput.txt","a") as f:
                            f.write(str(response.url)+"\n")
                    #API Request Method e.g. GET, PUT etc 
                    message += "Request Method: "+ str((responseReq).method)+"\n"
                    #Request Headers
                    message += "Request Headers: \n"+ str(responseReq.headers)+"\n"
                    #Response Headers
                    message += "Response Headers: \n"+ str(response.headers)+"\n"
                    #Response Reason e.g. OK
                    message += "Response Reason: "+str(response.reason)+"\n"
                    
            #happens if the api returns an image     
            except ValueError:
                responseReq = response.request
                #Normal Response e.g. 200, 300, 400
                message += "\nResponse: "+ str(response)+"\n"
                #API Response URL
                message += "Response Path: "+ str(response.url)+"\n"
                print("URL Accepted: ",response.url,"\n\n")
                with open("acceptedLinks.txt","a") as f:
                    f.write(str(response.url)+"\n")
                aLO = getWordlist("acceptedLinksOutput.txt")
                
                if (str(response.url)) not in aLO:
                    with open("acceptedLinksOutput.txt","a") as f:
                        f.write(str(response.url)+"\n")
                #API Request Method e.g. GET, PUT etc 
                message += "Request Method: "+ str((responseReq).method)+"\n"
                #Request Headers
                message += "Request Headers: \n"+ str(responseReq.headers)+"\n"
                #Response Headers
                message += "Response Headers: \n"+ str(response.headers)+"\n"
                #Response Reason e.g. OK
                message += "Response Reason: "+str(response.reason)+"\n"

            #JSON Response
            #for i in range(len((response.json()))):
                #print("Request Response:",i," ",(response.json())[i],"\n")#this is aan example json() files are stored as lists. 

        return message
        

    except NameError:
        print ("NameError! Please check the link. (IMGs can cause this error)")
        sys.exit()
    
#for loop functions to discover API names using a predefined word list. 
def apiReq(urlLink, wordlistPath):
    #get the wordlist that was specified by the user and put it into a variable to call later
    wordlist = getWordlist(wordlistPath)

    #initial testing for links 
    for i in wordlist:
        tempLink = urlLink + i
        output = apiDetails(tempLink)
        if output != None: 
            with open("output.txt","a") as f:
                print(tempLink) #uncomment this when you want to test the links and whether it is iterating the list 
                f.write(output)
    #further looping of links            
    apiDetailsFromAcceptedLinks(wordlist)
    main()
    return "Process Complete"


@timeoutable()
def main():
    
    url = ""
    fileName = ""
    flag = True
    try:
        usrInput = input("Enter a command (type -h for help): ")
        while flag == True:
            if (usrInput.split())[0] == "-h":
                print("\nThis is the ApiDiscovery Tool Help Page!\n"
                      "----------------------------------------------------------------------------------------------\n"
                      "-h          This is to bring up the help page for the application.\n"
                      "-u          This command is to be accompanied by a url that you want to test.\n"
                      "-w          This command is to specify the wordlist you would want to use for the application.\n"
                      "check       This command is to check the url and/or wordlist that was/were set.\n"
                      "run         This command is to run the program after the variables have been set."
                      "-q          This command is to quit the application\n"
                      "-----------------------------------------------------------------------------------------------")
                usrInput = input("Enter a command (type -h for help): ")
                
            elif (usrInput.split())[0] == "-u":
                if url == "":
                    url = input("Please enter the url you want to scan: ")
                    #if url[::-1] != "/":
                        #url = url+"/"
                        #print(url)
                else:
                    print("You have already inputed a url!")
                    userInput = (input("Do you want to re-enter your previous URL?(Yes/No): ")).lower()
                    flag = False
                    while flag == False:
                        if userInput == "yes":
                            url = input("Please enter the url you want to scan: ")
                            flag = True
                        elif userInput == "no":
                            print("Continuing Execution..")
                            flag = True
                        else:
                            print("Error Please type in only yes and no")
                            userInput = (input("Do you want to re-enter your previous URL?(Yes/No): ")).lower()
                            
                usrInput = input("Enter a command (type -h for help): ")

            elif (usrInput.split())[0] == "-w":
                if fileName == "":
                    fileName = input("Please input the file name for the wordlist you want to use: ")
                else:
                    print("You have already inputed a file path!")
                    userInput = (input("Do you want to re-enter your previous file path?(Yes/No): ")).lower()
                    flag = False
                    while flag == False:
                        if userInput == "yes":
                            fileName = input("Please input the file name for the wordlist you want to use:  ")
                            flag = True
                        elif userInput == "no":
                            print("Continuing Execution..")
                            flag = True
                        else:
                            print("Error Please type in only yes and no")
                            userInput = (input("Do you want to re-enter your previous file path?(Yes/No): ")).lower()

                usrInput = input("Enter a command (type -h for help): ")

            elif (usrInput.split())[0] == "check":
                if (url != "" and fileName != ""):
                    print("Url: ", url)
                    print("Wordlist: ", fileName)
                    
                else:
                    print("You have not set your url and/or wordlist!")
                usrInput = input("Enter a command (type -h for help): ")
                
            elif (usrInput.split())[0] == "run":
                if url == "" and fileName == "":
                    print("ERROR! Please check that you have entered your url and filename for the program to work!")
                    usrInput = input("Enter a command (type -h for help): ")
                else:
                    apiReq(url,fileName)
                    flag = False
            elif (usrInput.split())[0] == "-q":
                flag = False

            else:
                print("Please check your inputs! Type help if you need the list of commands!")
                usrInput = input("Enter a command (type -h for help): ")
    except ValueError:
            print("Please check your inputs!")
            usrInput = input("Enter a command (type -h for help): ")
    return "Program Ended"  

clearLogs()
#timeout function for python script set to 1 hour timeout in seconds (3600)
try:
    result = main(timeout = 3600)
    print("Timeout. Execution Reached its Limit of 1 hour. Check the code to change the default value. Default value: 3600")

except:

    print("Timeout. Execution Reached its Limit of 1 hour. Check the code to change the default value. Default value: 3600")



    

