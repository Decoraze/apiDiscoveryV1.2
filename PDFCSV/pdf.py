#imports
from datetime import datetime
import os
import jinja2 #pip
import pdfkit #pip

#inititalise lists for variables
subDomainList = []
httpxList = []
feroxList = []
nucleiList = []

def fileCheck(filePath):
    fileInput = False
    while fileInput == False:
        try:
            file = open(filePath)

            fileInput = True
            return True
            
        except FileNotFoundError:
            
            return False


def pdfOutput(url,subFinder,httpx,feroxbuster,nuclei):
    #initialise variables for pdf
    Website_URL = url
    subDomainResults = subFinder
    httpxResults = httpx
    feroxBusterResults = feroxbuster
    nucleiResults = nuclei
    dateTime = datetime.today().strftime("%d-%b-%Y %H%M%S")


    context = {'Website_URL': Website_URL, 'subDomainResults':subDomainResults, "httpxResults":httpxResults,
     "feroxBusterResults":feroxBusterResults,"nucleiResults":nucleiResults,"dateTime":dateTime}
    
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template("PDFCSV/pdf.html")
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    output_pdf = (url+dateTime+'.pdf')

    pdfkit.from_string(output_text, output_pdf, configuration=config,css="PDFCSV/style.css")
    #print('done')
    return None

def insertValues(sub,httpx,ferox,nuclei,url):
    urlOutput = url
    subDomainOutput = ''                                                                  #                       add website url that was scanned to the template
    httpxOutput = ''
    feroxOutput = ''
    nucleiOutput = ''

    for value in sub:
        subDomainOutput += (str(value)+"<br> ")                                           #                       append subdomains to the string for the output for the pdf file

    for value in httpx:                                                                   #                       append httpx values to the string
        httpxOutput += (str(value)+"<br> ")                                               #                       add <br> (spacing) to the string for newline in html/pdf

    for value in ferox:                                                                   #                       append httpx values to the string
        feroxOutput += (str(value)+"<br> ")                                               #                       add <br> to the string for newline in html

    for value in nuclei:
        nucleiOutput += (str(value)+"<br> ")

    pdfOutput(urlOutput,subDomainOutput,httpxOutput,feroxOutput,nucleiOutput)

def findUrl(subdomains,path):

    acceptedUrls = []                                                                     #                        create a temp list to populate with the urls. 
    #read directory
    directory_list = os.listdir(path)                                                     #                        read the directory items (including folders)                                                                #                        
    for listDir in subdomains:                                                            #                        enumerate through subdomains given to find the commanality for the urls
        tempFileName = listDir+"Feroxbuster.txt"                                          #                        concat the directory with feroxbuster.txt to find the common one. 
        if tempFileName in directory_list:                                                #                        if common, append it to the temp list
            acceptedUrls.append(listDir)                                                  #                        ^^^

    return acceptedUrls

#function for populating the lists 
def getResults(fileName,link):

    #appending subfinder results from the text file into a list.
    subfinderDir = ('toolsOutput/finalFindings/'+fileName+"/"+link+"Subfinder.txt")        #                        directory listing for the text file
    openSubFinder = open(subfinderDir)                                                     #                        opening subfinder text file
    for line in openSubFinder:                                                             #                        reading subfinder file line by line
        line = line.replace('\n','')                                                       #                        remove newline character before appending
        subDomainList.append(line)                                                         #                        appending results to subfinder list 
    #print(subDomainList)#delete this aft testing


    #appending httpx results from the text file into the list. 
    httpxDir = ('toolsOutput/finalFindings/'+fileName+"/"+link+"Httpx.txt")                #                        directory listing for the httpx file
    openHttpx = open(httpxDir)                                                             #                        opening httpx text file
    for line in openHttpx:                                                                 #                        reading opened file line by line
        line = line.replace('\n','')                                                       #                        replacing newline character before appending
        line = line.split(" ")                                                             #                        making the line into a list for filtering
        httpxList.append(str(line[0])+str(line[3::]))                                      #                        appending results to httpx list
    #print(httpxList)

    #get urls 
    acceptedUrls = findUrl(subDomainList,('toolsOutput/finalFindings/'+fileName+"/"))
    #print(acceptedUrls)
    
    #whitelisted sites
    usr = False
    whiteList = []
    while usr == False:
        try:
            usrInput = str(input("Please input your text file path for whitelisted sites:"))
            if usrInput == "":
                usr = True
            else:

                if fileCheck(usrInput) == True:
                    f = open(usrInput)
                    
                    for line in f:
                        line = line.replace('\n','')
                        whiteList.append(line)
                    usr = True
                elif fileCheck(usrInput) == False:
                    print("File Not Found!! Please enter again")

                else:
                    print("An error has occured!")
            
        except FileNotFoundError or ValueError:
            print("Error has occured! Please check your inputs")

    #appending ferox result from the text file into the list
    for x in acceptedUrls:                                                               #                       enumerate through the list of accepted urls(urls that were scanned) 
        feroxbuster_file = ('toolsOutput/finalFindings/'+fileName+"/"+x+"Feroxbuster.txt")#                      directory listing for the feroxbuster file
        openFerox = open(feroxbuster_file)                                                  #                       opening feroxbuster text file for specified url
        for line in openFerox:                                                              #                       reading opened file line by line
            line = line.replace('\n','')                                                    #                       replacing newline character before appending 
            feroxList.append(line)                                                          #                       appending results to ferox list
    #print(feroxList)

    #update links in pdf
    for i in whiteList:
        for line in feroxList:
            if i in line:
                feroxList.remove(line)

    for x in acceptedUrls:                                                               #                       enumerate through the list of accepted urls(urls that were scanned)
        nuclei_file = ('toolsOutput/finalFindings/'+fileName+"/"+x+"Feroxbuster.txtNucleiOutput.txt")#           directory listing for the nuclei file
        openNuclei = open(nuclei_file)                                                      #                       opening nuclei text file for specified url
        for line in openNuclei:                                                             #                       reading opened file line by line
            line = line.replace('\n','')                                                    #                       replacing newline character before appending 
            nucleiList.append(line)                                                         #                       appending results to nuclei list
    #print(nucleiList)

    insertValues(subDomainList,httpxList,feroxList,nucleiList,link)
    #print("open")
    return None

#function for populating the variables to prepare for pdf




def main(filedir,url):
    getResults(filedir,url)
    
    return None

#main("thedogapi.com224418","thedogapi.com")