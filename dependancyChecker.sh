#!/bin/bash

##Version/Downloaded Check##
nucleiCheck=`dpkg -l | grep nuclei`
subfinderCheck=`dpkg -l | grep subfinder`
feroxbusterCheck=`dpkg -l | grep feroxbuster`
golangCheck=`dpkg -l | grep golang`
wkhtmltopdfCheck=`dpkg -l | grep wkhtmltopdf`

##Checking Nuclei##
if [ -z "$nucleiCheck"  ]
then
	echo "Nuclei is NOT installed in your system. Installing Nuclei....."
	echo ""
	sudo apt-get install nuclei
else
	echo "Nuclei is Installed in your system."
fi	
##Checking Subfinder##
if [ -z "$subfinderCheck" ]
then
	echo "Subfinder is NOT installed in your system. Installing subfinder....."
	echo ""
	sudo apt install subfinder 
	sudo go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
else
	echo "Subfinder is installed in your system."
fi
##Checking Feroxbuster##
if [ -z "$feroxbusterCheck" ]
then
	echo "Feroxbuster is NOT installed in your system. Installing feroxbuster....."
	echo ""
	sudo apt install feroxbuster
else
	echo "Feroxbuster is installed in your system."
fi
##Checking GoLang##
if [ -z "$golangCheck" ]
then
	echo "GoLang is NOT installed in your system. Installing golang......"
	echo ""
	sudo apt-get install golang
else
	echo "GoLang is installed in your system."
fi

##Checking wkhtmltopdf
if [ -z "$wkhtmltopdfCheck" ]
then
	echo "WKHTMLtoPDF is NOT installed in your system. Installing wkhtmltopdf......"
	echo ""
	sudo apt-get install wkhtmltopdf
else
	echo "WKHTMLTOPDF is installed in your system"
fi
echo ""

echo "### Error whilst finding httpx in your system. Installing HTTPX  ###"
sudo apt-get remove python3-httpx
sudo git clone https://github.com/projectdiscovery/httpx.git
cd httpx/cmd/httpx
sudo go build
sudo mv httpx /usr/local/bin/
cd ../../../
sudo rm -r httpx 

#download Python Libraries
sudo pip3 install pdfkit																					

sudo pip3 install argparse																					

sudo pip3 install datetime																		

sudo pip3 install jinja2










