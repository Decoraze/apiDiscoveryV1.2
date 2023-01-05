#!/bin/bash

##Version/Downloaded Check##
nucleiCheck=`dpkg -l | grep nuclei`
subfinderCheck=`dpkg -l | grep subfinder`
feroxbusterCheck=`dpkg -l | grep feroxbuster`
golangCheck=`dpkg -l | grep golang`


##Checking Nuclei##
if [ -z "$nucleiCheck"  ]
then
	echo "Nuclei is NOT installed in your system. Installing Nuclei....."
	echo ""
	apt-get install nuclei
else
	echo "Nuclei is Installed in your system."
fi	
##Checking Subfinder##
if [ -z "$subfinderCheck" ]
then
	echo "Subfinder is NOT installed in your system. Installing subfinder....."
	echo ""
	apt-get install subfinder
else
	echo "Subfinder is installed in your system."
fi
##Checking Feroxbuster##
if [ -z "$feroxbusterCheck" ]
then
	echo "Feroxbuster is NOT installed in your system. Installing feroxbuster....."
	echo ""
	apt-get installferoxbuster
else
	echo "Feroxbuster is installed in your system."
fi
##Checking GoLang##
if [ -z "$golangCheck" ]
then
	echo "GoLang is NOT installed in your system. Installing golang......"
	echo ""
	apt-get install golang
else
	echo "GoLang is installed in your system."
fi
echo ""
echo "### Error whilst finding httpx in your system. Installing HTTPX  ###"
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
