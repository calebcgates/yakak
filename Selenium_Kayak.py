#####
###
### SETUP

###Chrome Drivers
###Check you have installed latest version of chrome brwoser-> chromium-browser -version
###If not, install latest version of chrome sudo apt-get install chromium-browser
###get appropriate version of chrome driver from here
###Unzip the chromedriver.zip
###Move the file to /usr/bin directory sudo mv chromedriver /usr/bin
###Goto /usr/bin directory and you would need to run something like chmod a+x chromedriver to mark it #executable.
###finally you can execute the code.

#>> sudo pip install selenium
#>> sudo pip install pyvirtualdisplay
#>> sudo apt install chromium-browser
#>> pip install twilio

###
###
#####

#####
###
### TO RUN

#>> python Selenium_Kayak.py

###
###
#####

#####
###
### CONFIG

## CONFIG VARIABLES
## Pushing a slower wait time will make the program run faster.  dont want to push beyond the load speed of the page.  Not sure if python continues to execute before the driver.get loads the entire page...  I beleive it doesnt exicute until the entire page loads which means there is no reason to wait very long
wait_time = 1 #1second when accessing the website
## Sleep Time Before Rerunning
sleep_time = 60*5 #seconds

## must tailor os. locations to your computer
user_actn = "caleb"

## FLight Data
loc1 = "BDL"
loc2 = "HKG"	#"LAX"
date1 = "2017-04-18"
date2 = "2017-04-22"

##Alert Price
alertPrice = 600

###
###
#####

###for testing
import sys
### for file system
import os
import os.path
###FOR JS Driver and execute script
from selenium import webdriver
###for waiting
import time
###for output data reading
import json
from pprint import pprint
###for interpreting JSON
import re
### TWILLIO TEXT ALERTS
from twilio.rest import TwilioRestClient


	### Pushing a slower wait time will make the program run faster.  dont want to push beyond the load speed of the page.  Not sure if python continues to execute before the driver.get loads the entire page...  I beleive it doesnt exicute until the entire page loads which means there is no reason to wait very long
wait_time = 1
before_scrape_time = 5

###remove data file
file_path = "/home/"+user_actn+"/Downloads/data.json"

### When looping if price alert zone = 1 you're alreay ina price alert so dont text the user continusously.  Text them when the price alert ends
priceAlertZone = 0  #Zone:0 == Price is not below LowPrice,   Zone:1 == Price is currently below low price - Do Not Retext User,  Text when zone changes back to Zone:0


while(1):

	if os.path.exists(file_path):
		os.remove(file_path) 

	chromedriver = "/usr/bin/chromedriver"
	os.environ["webdriver.chrome.driver"] = chromedriver
	driver = webdriver.Chrome(chromedriver)
	driver.get("https://www.kayak.com/flights/"+loc1+"-"+loc2+"/"+date1+"/"+date2)

	#driver.execute_script("window.alert('this is an alert')") ###UNIT TEST
	 
	#WANT TO LOAD LOCAL RESOURCE BUT NOT ALLOWED - WORK AROUND? PERMISSIONS?
		#url = ~/Desktop/Kayak/artoo-latest.min.js; ?? DOESNT WORK NEED TO GET SCRIPT FROM MY COMPUTER???
		#url = "//medialab.github.io/artoo/public/dist/artoo-latest.min.js";  CURRENT WORKS
		#url = "file:///home/caleb/Desktop/Kayak/artoo-latest.min.js";     #NOT ALLOWD TO LOAD LOCAL RESOURCE:  ?? WHY ## NICE TO HAVE BUT STILL WORKS WITH GITHUB SCRIPT LOAD

	time.sleep(wait_time) #not sure i need to wait here, may not exicute until page loads entirely...  
	###Want to edit the url = to be a local file to prevent github spaming downloading this project/script
	driver.execute_script("""
	var script = document.createElement( 'script' );
	script.type = 'text/javascript';
	url = "//medialab.github.io/artoo/public/dist/artoo-latest.min.js";
	script.src = url;
	$("body").append( script );
	""")
	###pause because not running if I do back to back.  Gives time for artoo to load/ or kayak request timeout?
	time.sleep(before_scrape_time)  
	###getting prices by class and saving as a file that python can access 
	driver.execute_script("""
	artoo.scrape('.bigPrice', {
	  content: 'text'
	}, artoo.savePrettyJson);
	""")

	time.sleep(wait_time) #enough time to download?
	### Closes the chrome instance
	driver.quit()


	### Print Prices If Downloaded Properly
	if os.path.exists(file_path):
		with open(file_path) as data_file:    
		    data = json.load(data_file)
		    ###pprint(data) will print data array but not needed
		###THIS FOR LOOP IS UNNECESARY Just prints to the terminal all prices	
		##for num in range(0,len(data)):
		##	price1 = data[num]["content"]
		##	price1 = price1[1:]
		##	print(price1)

		lowPrice = data[0]["content"]
		lowPrice = lowPrice[1:]
		print('Low Price:'+lowPrice)
		#print(float(lowPrice))	
		if(float(lowPrice) <= alertPrice and priceAlertZone == 0):
			priceAlertZone = 1
			print('Zone:'+str(priceAlertZone))
			###TWILIO
			### put your own credentials here
			ACCOUNT_SID = 'ACbd3283ed65be0d347aa621dd4fbac5d8'  #'<AccountSid>'
			AUTH_TOKEN = '27cc9d1a87b03c7e203d952a0307be5a'  #'<AuthToken>'
			client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
			client.messages.create(
			to =    '8607597185',	#'<ToNumber>',
			from_ = '8609692659',	#'<FromNumber>',
			body =  'PYTHON: LOWEST PRICE IS:'+str(lowPrice),	#'<BodyText>',
			)
		elif(float(lowPrice) >= alertPrice and priceAlertZone == 1):
			priceAlertZone = 0
			print('Zone:'+str(priceAlertZone))
			ACCOUNT_SID = 'ACbd3283ed65be0d347aa621dd4fbac5d8'  #'<AccountSid>'
			AUTH_TOKEN = '27cc9d1a87b03c7e203d952a0307be5a'  #'<AuthToken>'
			client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
			client.messages.create(
			to =    '8607597185',	#'<ToNumber>',
			from_ = '8609692659',	#'<FromNumber>',
			body =  'Your Low Price Has Ended:'+str(lowPrice),	#'<BodyText>',
			)
		elif(priceAlertZone == 1):
			#print("continued price alert zone")
			print("Zone:1")

	else:
		print("file did not download properly")


	### Exit program
	time.sleep(sleep_time)

sys.exit()







### ORIGINAL ARTOO INJECTION SCRIPT BOOKMARKLET
#'(function(){var t={},e=!0;if("object"==typeof this.artoo&amp;&amp;(artoo.settings.reload||(artoo.log.verbose("artoo already exists within this page. No need to inject him again."),artoo.loadSettings(t),artoo.exec(),e=!1)),e){var o=document.getElementsByTagName("body")[0];o||(o=document.createElement("body"),document.documentElement.appendChild(o));var a=document.createElement("script");console.log("artoo.js is loading..."),a.src="//medialab.github.io/artoo/public/dist/artoo-latest.min.js",a.type="text/javascript",a.id="artoo_injected_script",a.setAttribute("settings",JSON.stringify(t)),o.appendChild(a)}}).call(this);' 

### CONVERTING SCRIPT TO JQUERY
#var o=document.getElementsByTagName("body")[0]
#o=document.createElement("body")
#document.documentElement.appendChild(o))
##var a=document.createElement("script")
#console.log("artoo.js is loading...")
#a.src="//medialab.github.io/artoo/public/dist/artoo-latest.min.js"
#a.type="text/javascript"
#a.id="artoo_injected_script"
#a.setAttribute("settings",JSON.stringify(t))
#o.appendChild(a)
#o=document.createElement("body")
#document.documentElement.appendChild(o))
#var a=document.createElement("script")
#console.log("artoo.js is loading...")
#a.src="//medialab.github.io/artoo/public/dist/artoo-latest.min.js"
#a.type="text/javascript"
#a.id="artoo_injected_script"
#a.setAttribute("settings",JSON.stringify(t))
#o.appendChild(a)

### FINAL FORM
works = """var script = document.createElement( 'script' );
script.type = 'text/javascript';
url = "//medialab.github.io/artoo/public/dist/artoo-latest.min.js";
script.src = url;
$("body").append( script );
"""
