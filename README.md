Welcome to API Endpoint Discovery!

# Setup

Remember to use python3 to run this file along side kali linux.

List of tools to download:
- Subfinder: [https://github.com/projectdiscovery/subfinder](https://github.com/projectdiscovery/subfinder),
- Nuclei: [https://github.com/projectdiscovery/nuclei](https://github.com/projectdiscovery/nuclei),
- HTTPx: [https://github.com/projectdiscovery/httpx](https://github.com/projectdiscovery/httpx),
- Feroxbuster: sudo apt-get install feroxbuster,
- Wkhtmltopdf: sudo apt-get install wkhmtltopdf,

Python Libraries to Download or Check for Availibility:
- Subprocess
- Argparse
- datetime
- jinja2
- pdfkit

To download python libraries you can use the pip3 install command in command line. 


# Features

To run it, run the "apiDiscovery.py" file using python3 e.g. python3 apiDiscovery.py ..... 
There are 3 options at the moment.


1) t: to use the tools for scanning

2) -h: to bring up the help page
3) q: to quit the program


# How to run:

bash
python3 apiDiscovery.py [url to use e.g. google.com,twitter.com,thedogapi.com,megacorpone.com] [choice: t,q,-h] 



e.g. 

python3 apiDiscovery.py thedogapi.com t (to scan thedogapi.com and to use the tools for scanning the uri  



****Note: do not need to use any subdomains like [www.xxx.com](http://www.xxx.com/), [https://api.xxx.com](https://api.xxx.com/) etc****


# Problems

If you run into any problems email me at aureliusng@bdo.com.sg the issues along with the screenshot of said issue. 

Thanks!
